use crate::{ZZ, zz};
use std::collections::HashMap;


fn smod(a: impl AsRef<ZZ>, m: impl AsRef<ZZ>) -> ZZ {
    let a = a.as_ref();
    let m = m.as_ref();

    (a % m + m) % m
}

pub fn gcd(a: impl AsRef<ZZ>, b: impl AsRef<ZZ>) -> ZZ {
    let a = a.as_ref();
    let b = b.as_ref();

    a.gcd(b)
}
pub fn egcd(a: impl AsRef<ZZ>, b: impl AsRef<ZZ>) -> (ZZ, ZZ, ZZ) {
    let a = a.as_ref();
    let b = b.as_ref();

    a.egcd(b)
}

pub fn crt(v: impl AsRef<Vec<ZZ>>, m: impl AsRef<Vec<ZZ>>) -> (ZZ, ZZ) {
    let v = v.as_ref();
    let m = m.as_ref();

    assert_eq!(v.len(), m.len(), "v.len() != m.len()");

    let mut n = zz!(1);
    let mut x = zz!(0);
    for i in 0..v.len() { n *= &m[i]; }
    for i in 0..v.len() {
        let l = &n/&m[i];
        let (_, _, y) = egcd(&m[i], &l);
        x += &v[i] * &y * &l;
    }
    (smod(&x, &n), n)
}

pub fn mod_inv(g: impl AsRef<ZZ>, m: impl AsRef<ZZ>) -> Option<ZZ> {
    let m = m.as_ref();

    let (d, x, _) = egcd(g, m);
    if d == 1 {
        Some(smod(&x, m))
    } else {
        None
    }
}

pub fn totient(primes: impl AsRef<[ZZ]>) -> ZZ {
    let primes = primes.as_ref();


    let mut map = HashMap::new();
    for p in primes.iter() {
        let v = map.entry(p).or_insert(0);
        *v += 1;
    }

    let mut out = zz!(1); 
    for (prime, count) in map.iter() {
        out *= prime.pow(*count-zz!(1));
        out *= *prime - 1;
    }
    out
}

pub fn continued_fraction(x: impl AsRef<ZZ>, y: impl AsRef<ZZ>) -> Vec<(ZZ, ZZ)> {
    let mut x = x.as_ref().clone();
    let mut y = y.as_ref().clone();

    let mut a = &x/&y;
    let mut out = vec![(a.clone(), zz!(1))];

    while &(&a * &y) != &x {
        std::mem::swap(&mut x, &mut y);
        y = &y - &a * &x;
        a = &x / &y;

        if out.len() == 1 {
            let n = &a * &out[0].0 + 1;
            let d = &a * 1;
            out.push((n, d));
        }
        else if out.len() == 2 {
            let n = &a * &out[1].0 + &out[0].0;
            let d = &a * &out[1].1 + 1;
            out.push((n, d));

        }
        else {
            let n = &a * &out[out.len()-1].0 + &out[out.len()-2].0;
            let d = &a * &out[out.len()-1].1 + &out[out.len()-2].1;
            out.push((n, d));
        }
    }
    out
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_mod_inv() {
        let (g, m) = (zz!(123), zz!(937));
        assert_eq!(mod_inv(g, m).unwrap(), zz!(678));
    }

    #[test]
    fn test_crt() {
        let m = vec![zz!(678255406928205283764318788009),
			         zz!(206668822692514401698496953701), 
			         zz!(209389899037793911571890084709)];
        let v = vec![zz!(553595583601907102790863048168),
			         zz!(179936685740203889915724224774),
			         zz!(118574769100120356915050028243)];
        let sol = (zz!(11729333136918336599556614225262019449383649885811789858959155083082618000073636325423824), 
			         zz!(29351071308657422647975598374376392562718985574346423618982742115523312472944466642614081));

        assert_eq!(crt(&v, &m), sol);
    }

    #[test]
    fn test_totient() {
        let factors = &[zz!(61), zz!(61), zz!(2113), zz!(3624601)];

        assert_eq!(totient(factors), zz!(28017868032000));
    }

    #[test]
    fn test_continued_fraction() {
        assert_eq!(continued_fraction(zz!(123), zz!(2)), vec![zz!((61, 1)), zz!((123, 2))]);
        assert_eq!(continued_fraction(zz!(123127308098), zz!(202187)), vec![zz!((608977, 1)), zz!((1217955, 2)), zz!((1826932, 3)), zz!((4871819, 8)), zz!((35929665, 59)), zz!((256379474, 421)), zz!((292309139, 480)), zz!((2594852586, 4261)), zz!((28835687585, 47351)), zz!((31430540171, 51612)), zz!((123127308098, 202187))]);
    }
}
