use num::bigint::{BigInt, Sign::Plus};
use num::{Signed, Zero, One};
use std::fmt;
use std::iter::Sum;
use std::str::FromStr;

#[derive(Clone, Hash)]
pub struct ZZ {
    pub(super) v: BigInt,
}

impl ZZ {
    pub fn zz_from_str(s: &str) -> Result<ZZ, ()> {
        match BigInt::from_str(s) {
            Ok(v) => {
                return Ok(ZZ { v });
            }
            Err(_) => return Err(()),
        };
    }
}

impl ZZ {
    pub fn abs(mut self) -> Self {
        if self.v.is_negative() {
            self *= -1;
            return self;
        }
        self
    }

    pub fn neg(self) -> Self {
        return -self;
    }

    pub fn to_string(&self) -> String {
        self.v.to_string()
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        self.v.to_signed_bytes_be()
    }

    pub fn one() -> ZZ {
        ZZ { v: BigInt::one() }
    }
    pub fn zero() -> ZZ {
        ZZ { v: BigInt::zero() }
    }

    pub fn from_bytes_be(bytes: &[u8]) -> ZZ {
        ZZ { v: BigInt::from_bytes_be(Plus, bytes) }
    }

    pub fn bits(&self) -> u64 {
        self.v.bits()
    }

}

impl AsRef<ZZ> for ZZ {
    fn as_ref(&self) -> &ZZ {
        self
    }
}

impl fmt::Debug for ZZ {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.v.to_string())
    }
}
impl fmt::Display for ZZ {
    // Required method
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.v.to_string())
    }
}

impl Sum for ZZ {
    fn sum<T>(iter: T) -> Self
    where
        T: Iterator<Item = ZZ>,
    {
        iter.fold(ZZ { v: BigInt::from(0) }, |a, b| ZZ { v: a.v + b.v })
    }
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn basic() {
        let v: Vec<i32> = [-2, -1, 0, 1, 2, 21302183, 3612321].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                if t1 == t2 {
                    continue;
                }
                assert_ne!(ZZ::from(t1), ZZ::from(t2));
            }
        }
        for &t1 in v.iter() {
            assert_eq!(ZZ::from(t1), ZZ::from(t1));
        }
    }
}
