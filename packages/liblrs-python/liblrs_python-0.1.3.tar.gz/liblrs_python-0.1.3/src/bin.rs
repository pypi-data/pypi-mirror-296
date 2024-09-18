use liblrs::lrs::Lrs;
use liblrs::lrs_ext::ExtLrs;

fn main() {
    Lrs::<liblrs::curves::SphericalLineStringCurve>::new("python/osm.pbf").expect("moo");
}
