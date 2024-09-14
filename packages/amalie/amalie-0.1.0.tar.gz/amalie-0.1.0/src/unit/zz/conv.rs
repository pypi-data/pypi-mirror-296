use super::ZZ;
use num::bigint::BigInt;
use crate::{Result, Error};
use std::convert::TryFrom;
use std::str::FromStr;

macro_rules! impl_from_type {
    ($($type:ident),*) => {
        $(
            impl From<$type> for ZZ {
                fn from(item: $type) -> Self {
                    ZZ {
                        v: BigInt::from(item),
                    }
                }
            }
        )*
    }
}

impl_from_type!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128, BigInt);

impl From<ZZ> for BigInt {
    fn from(value: ZZ) -> Self {
        value.v.clone()
    }
}


impl FromStr for ZZ {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self> {
        match BigInt::from_str(s) {
            Ok(v) => Ok(ZZ { v }),
            Err(_) => Err(Error::CouldNotParse),
        }
    }
}

macro_rules! impl_try_from {
    ($($type:ident),*) => {
        $(
            impl TryFrom<&ZZ> for $type {
                type Error = Error;

                fn try_from(value: &ZZ) -> Result<Self> {
                    match (&value.v).try_into() {
                        Ok(v) => Ok(v),
                        Err(_) => Err(Error::CouldNotConvert),
                    }
                }
            }
        )*
    }
}

impl_try_from!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);
