use crate::{Error, Result, zz, ZZ, alg::gcd};

fn g(mut x: ZZ) -> ZZ {
    x <<= 1;
    x += 1;
    x
}
pub fn pollard_rho(n: impl AsRef<ZZ>) -> Result<ZZ> {
    let n = n.as_ref();
    if n < 2 {
        return Err(Error::InvalidInput("n < 2".to_string()));
    }

    let mut x = zz!(2);
    let mut y = x.clone();
    let mut d = zz!(1);
    while &d == 1 {
        x = g(x);
        y = g(g(y));
        d = gcd((&x-&y).abs(), n)
    }
    if &d == n {
        return Err(Error::NoResult);
    }
    else {
        return Ok(d);
    }
}

#[cfg(test)]
mod test {
    use super::pollard_rho;
    use crate::{zz, ZZ};

    #[test]
    fn test_pollard_rho() {
        assert_eq!(pollard_rho(zz!(123)).unwrap(), 3);
        assert_eq!(pollard_rho(zz!(1)).is_err(), true);
        assert_eq!(pollard_rho(zz!(2)).is_err(), true);
        assert_eq!(pollard_rho(zz!(6131066257801)).unwrap(), 19);
    }
}
