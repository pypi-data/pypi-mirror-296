import json
import yaml
import click
import math
from enum import Enum, auto

from liblrs_python import Builder, Point, AnchorOnLrm

# This script merges three datasources to build a full LRS for the French railway network
# - OpenStreetMap for the geometries
# - OSRD’s dataset for anchors geometry
# - Gaia for the distances between anchors

class VoieRkMatching(Enum):
    PERFECT_MATCH = auto()
    FALLBACK = auto()
    NOT_FOUND = auto()

class VoieSNCF:
    def __init__(self, id, lrs_index):
        # The OSM id is in the form ref:FR:SNCF_Reseau="530000,1,UNIQUE,77.299,178.061"
        # We extract the different parts of the data
        [self.unpadded_ligne, self.tronçon, self.voie, pk_debut, pk_fin] = id.split(',')
        
        self.ligne = self.unpadded_ligne.rjust(6, '0')
        self.id = f"{self.ligne},{self.tronçon},{self.voie},{pk_debut},{pk_fin}"
        self.lrs_index = lrs_index

        # Some RER-C weirdness where letters are used for anchors
        self.pk_debut = float(VoieSNCF.fix_letters(pk_debut))
        self.pk_fin = float(VoieSNCF.fix_letters(pk_fin))
        if self.pk_debut > self.pk_fin:
            self.pk_debut, self.pk_fin = self.pk_fin, self.pk_debut

        self.length = self.pk_fin - self.pk_debut
        self.anchors = []
        self.gaia_lrm = None

    def rk_id(self, anchor_indices):
        # Tries to find the _voie_ in the rk dataset
        # Looks for potential fallbacks if the name doesn’t fit exactly

        # The best case: everything matches perfectly
        rks_id = f"{self.ligne}-{self.tronçon}-{self.voie}"
        if rks_id in anchor_indices:
            return (VoieRkMatching.PERFECT_MATCH, rks_id)
        else:
            # We look for fallbacks by varing the the different elements
            # The goal is to find the most important _voie_ of the line as fallback
            for l in [self.ligne, self.unpadded_ligne]:
                for t in [self.tronçon, "1"]:
                    for v in [self.voie, "V1"]:
                        fallback = f"{l}-{t}-{v}"
                        if fallback in anchor_indices:
                            return (VoieRkMatching.FALLBACK, fallback)
        
        print(f"Could not find {self.id} in the rks, nor the fallbacks")
        return (VoieRkMatching.NOT_FOUND, None)
    
    def load_anchors(self, anchors, gaia_lrm):
        self.gaia_lrm = gaia_lrm
        for (name, index) in anchors.items():
            # We are not sure if `_begin` from gaia and `0` should be considered as the same
            # For now we decide to ignore them
            if name == "0": 
                continue

            if self.pk_debut <= float(name) <= self.pk_fin:
                if not name in gaia_lrm:
                    print(f"could not find anchor {name} in {gaia_id}")
                    continue
                distance = gaia_lrm.get(name) 
                self.anchors.append(AnchorOnLrm(index, distance))
    
    # Returns true if the curve of the traversal in the LRS has the same orientation as the RK
    # e.g. the milestone 400 must be before the milestone 410
    def correct_orientation(self, builder, anchor_coordinates):
        first_node_coord = anchor_coordinates[self.anchors[0].anchor_index]
        last_node_coord = anchor_coordinates[self.anchors[-1].anchor_index]

        return builder.project(self.lrs_index, first_node_coord) <= builder.project(self.lrs_index, last_node_coord)

    def fix_letters(pk):
        return pk.replace("D", "0").replace("E", "1").replace("F","2").replace("G", "3").replace("H", "4")

@click.command()
@click.option('--osm', help='OpenStreetMap source file in .pbf format')
@click.option('--gaia', help='Gaia data with distances between anchors as yaml.')
@click.option('--rks', help='SNCF RKs (anchors) as json.')
@click.option('--out', help='SNCF RKs (anchors) as json.')
def merge(osm, gaia, rks, out):
    # The LRS builder from liblrs. Every object that will be save must be built through it
    builder = Builder()

    # From OSM we read the topology (nodes, segments, traversals)
    builder.read_from_osm(
        input_osm_file=osm,
        lrm_tag="ref:FR:SNCF_Reseau",
        required=[("railway", "*")],
        to_reject=[]
    )

    # From GAIA we extract the distances between anchors
    gaia_lrms = {}
    with open(gaia) as gaia_lrs:
        gaia_lrs = yaml.safe_load(gaia_lrs)

        for gaia_lrm in gaia_lrs['linear_referencing_methods']:
            cumulated = 0
            distances = {}
            for i in range(1, len(gaia_lrm['distances'])): # We ignore _begin anchor
                anchor = gaia_lrm['anchors'][i]
                anchor_name = anchor.split('_')[1]
                cumulated += gaia_lrm['distances'][i]
                distances[anchor_name] = cumulated
            gaia_lrms[gaia_lrm['id']] = distances

    # From the RK file, we use the coordinates of the anchors and build the anchors
    anchor_indices = {}
    anchor_coordinates = []
    for track_id, rk_wrapper in json.loads(open(rks).read())['tracks'].items():
        anchor_indices[track_id] = {}
        rks = rk_wrapper['rks']

        for rk in rks:
            anchor_name = rk["name"]
            coord = Point(rk["location"]["lon"], rk["location"]["lat"])
            anchor = builder.add_anchor(
                id=f"{track_id}_{anchor_name}",
                name=rk["name"],
                coord=coord,
                properties={"source": rk["dataSet"]},
            );
            anchor_indices[track_id][anchor_name] = anchor
            anchor_coordinates.append(coord)

    # Some statistics to know how much we matched
    count_fallback = 0
    count_not_found = 0
    count_perfect_match = 0

    # When the curve is so short that there aren’t at least two anchors,
    # we can’t know how to orient them.
    # We store them until we have added all the oriented curves
    # and we use a reference traversal to deduce the orientation
    short_lrms = []
    # We store the reference traversal of a line
    # It will be used to deduce the orientation of small lrs
    lines_traversals = {}


    # We find what RK correspond to each traversal
    # Those will define the scale
    # We will also use them to re-orient the traversal
    # A bit later we will also add unamed anchors from OSM to have a finer scale

    # We orient the traversals with two methods
    # A. if we have at least two anchors (milestones from the RK file), we use their coordinates
    # B. otherwise, we project the extremities on the nearest line


    # We count how many named anchors (were we have the coordinates given by an external database)
    # If we have at least 2, it means we can use them to know the orientation
 
    # We now add the anchors (rk file), their distances (gaia) to traversals from OpenStreetMap
    voies = []
    for (osm_id, lrs_index) in builder.get_traversal_indexes().items():
        voie = VoieSNCF(osm_id, lrs_index)
        voies.append(voie)
        
        if voie.pk_fin == voie.pk_debut:
            print(f"Same start and end {voie.id}")
            continue

        (matching_result, rks_id) = voie.rk_id(anchor_indices)
        if matching_result == VoieRkMatching.PERFECT_MATCH:
            count_perfect_match += voie.length
        elif matching_result == VoieRkMatching.FALLBACK:
            count_fallback += voie.length
        else:
            count_not_found += voie.length
            # We give up, we won’t try to process this LRM
            continue
        
        # Try to find the distances from the gaia dataset. If we have the _voie_ we use it, otherwise fallback on the line
        gaia_id = f"{voie.ligne}_{voie.voie}" if f"{voie.ligne}_{voie.voie}" in gaia_lrms else voie.ligne
        gaia_lrm = gaia_lrms[gaia_id]
        voie.load_anchors(anchor_indices[rks_id], gaia_lrm)
        
        if len(voie.anchors) >= 2 and not voie.correct_orientation(builder, anchor_coordinates):
            builder.reverse(voie.lrs_index)

    # For the LRM where we don’t have two anchors, we try to find a “main” track to project onto
    # A main track must be from the same line and the PKs must be larger
    # If we don’t find any, me relax the PK constraint
    for voie in [voie for voie in voies if len(voie.anchors) < 2]:
        main_tracks = [main_track for main_track in voies if len(main_track.anchors) >= 2 and voie.ligne == main_track.ligne and voie.pk_debut >= main_track.pk_debut and voie.pk_fin <= main_track.pk_fin]
        if not main_tracks:
            print(f"Could not find main track for {voie.id}")
            main_tracks = [main_track for main_track in voies if len(main_track.anchors) >= 2 and voie.ligne == main_track.ligne]
        if not main_tracks:
            print(f"Could not find any other track of the line for {voie.id}")
            continue

        traversal_distances = [builder.euclidean_distance(voie.lrs_index, t.lrs_index) for t in main_tracks]
        nearest_traversal_indexes = [i for i, j in enumerate(traversal_distances) if j == min(traversal_distances)]
        main_track_index = main_tracks[nearest_traversal_indexes[0]].lrs_index

        nodes = builder.get_nodes_of_traversal(voie.lrs_index)
        first_node_coord = builder.get_node_coord(nodes[0])
        last_node_coord = builder.get_node_coord(nodes[-1])

        if builder.project(main_track_index, first_node_coord) > builder.project(main_track_index, last_node_coord):
            builder.reverse(voie.lrs_index)

    for voie in voies:
        # If we didn’t have any gaia distances, it is useless to try to have distances
        if not voie.gaia_lrm:
            continue
        # We add unnamed anchors that correspond to OSM nodes to improve the precision of the
        # We rely on the name of the name of the LRM to deduce the distance along the LRM
        # e.g. for the LRM 530000,1,UNIQUE,77.299,178.061
        #      that begins as a switch from the current traversal
        #      we add an unnamed anchor at distance 77+299 at its coordinates

        nodes_of_lrm = builder.get_nodes_of_traversal(voie.lrs_index)
        nodes_of_lrm_set = set(nodes_of_lrm)
        for (other_traversal_id, other_traversal_index) in builder.get_traversal_indexes().items():
            other_voie = VoieSNCF(other_traversal_id, other_traversal_index)
            # The line must be the same, otherwise the kilometric points aren’t measured the same
            if other_voie.ligne == voie.ligne and other_voie.id != voie.id:
                other_nodes = builder.get_nodes_of_traversal(other_traversal_index)
                first_node, last_node = other_nodes[0], other_nodes[-1]

                if first_node in nodes_of_lrm_set and voie.pk_debut < other_voie.pk_debut < voie.pk_fin:
                    anchor = builder.add_anchor(
                        id=f"crossing_{other_voie.id}_begin",
                        coord=builder.get_node_coord(first_node),
                        name=None,
                        properties={"source": "SNCF-OSM merge script (OSM node)"},
                    )

                    (other_begin_offset, other_begin_name) = math.modf(other_voie.pk_debut)

                    milestone = str(int(other_begin_name))
                    if milestone in voie.gaia_lrm:
                        distance_along_lrm = voie.gaia_lrm[milestone] + other_begin_offset * 1000
                        voie.anchors.append(AnchorOnLrm(anchor_index=anchor, distance_along_lrm=distance_along_lrm))
                    else:
                        print(f"Could not find milestone {milestone} in lrm {voie.id} when intersecting pk {other_voie.id}")
                
                if last_node in nodes_of_lrm_set and voie.pk_debut < other_voie.pk_fin < voie.pk_fin:
                    anchor = builder.add_anchor(
                        id=f"crossing_{other_voie.id}_end",
                        coord=builder.get_node_coord(last_node),
                        name=None,
                        properties={"source": "SNCF-OSM merge script (OSM node)"},
                    )

                    (other_begin_offset, other_begin_name) = math.modf(other_voie.pk_fin)
                    milestone = str(int(other_begin_name))
                    if milestone in voie.gaia_lrm:
                        distance_along_lrm = voie.gaia_lrm[milestone] + other_begin_offset * 1000
                        voie.anchors.append(AnchorOnLrm(anchor_index=anchor, distance_along_lrm=distance_along_lrm))
                    else:
                        print(f"Could not find milestone {milestone} in lrm {voie.id}")

        # Add unanamed anchors at the end of each traversal corresponding to have precise extremities based on OSM
        first_node, last_node = nodes_of_lrm[0], nodes_of_lrm[-1]
        (begin_offset, begin_name) = math.modf(voie.pk_debut)

        # Start of the LRM
        milestone = str(int(begin_name))
        if milestone in voie.gaia_lrm:
            first_distance_along_lrm = voie.gaia_lrm[milestone] + begin_offset * 1000
        else:
            first_distance_along_lrm = voie.pk_debut * 1000

        anchor = builder.add_projected_anchor(
                    id=f"{voie.id}_begin",
                    name=None,
                    position_on_curve=0,
                    properties={"source": "SNCF-OSM merge script (OSM node)"},
                )
        voie.anchors.append(AnchorOnLrm(anchor_index=anchor, distance_along_lrm=first_distance_along_lrm))

        # End of the LRM
        (end_offset, end_name) = math.modf(voie.pk_fin)
        milestone = str(int(end_name))
        if milestone in voie.gaia_lrm:
            last_distance_along_lrm = voie.gaia_lrm[milestone] + end_offset * 1000
        else:
            last_distance_along_lrm = voie.pk_fin * 1000

        anchor = builder.add_projected_anchor(
                    id=f"{voie.id}_end",
                    name=None,
                    position_on_curve=1,
                    properties={"source": "SNCF-OSM merge script (OSM node)"},
                )
        voie.anchors.append(AnchorOnLrm(anchor_index=anchor, distance_along_lrm=last_distance_along_lrm))

        # We add a virtual named anchor before the start
        # This allows to search for locations starting before the first anchor
        # e.g. The track goes from 100+200 to 101+200
        #      it distance along lrm is 1000, corresponding to `1.0` on the curve distance
        #      the distance from reference "100" to the first position on the curve is 200
        #      hence the reference "100" is at -0.2
        begin_name_str = str(int(begin_name))
        distance_along_lrm = first_distance_along_lrm - begin_offset * 1000
        anchor = builder.add_projected_anchor(
            id=f"{voie.id}_{begin_name_str}_extrapolated",
            name=f"{begin_name_str}",
            properties={"source": "SNCF-OSM merge script"},
            position_on_curve=-(first_distance_along_lrm - distance_along_lrm) / (last_distance_along_lrm - first_distance_along_lrm)
        )
        voie.anchors.append(AnchorOnLrm(anchor_index=anchor, distance_along_lrm=distance_along_lrm))
                
        builder.add_lrm(
                    id=voie.id,
                    traversal_index=voie.lrs_index,
                    anchors=voie.anchors,
                    properties={},
        )

    print(f"perfect match: {int(count_perfect_match)} km, fallback: {int(count_fallback)} km, not_found: {int(count_not_found)} km")

    builder.save(
        out,
        {
            "source": "OpenStreetMap",
            "licence": "OdBL",
        }
    )
    
if __name__ == "__main__":
    merge()