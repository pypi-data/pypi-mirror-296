use super::{zz,ZZ};
use crate::unit::macro_util::*;
use std::ops::{Mul, MulAssign};
use std::iter::Product;

impl<'a> Product<&'a ZZ> for ZZ {
    fn product<I>(iter: I) -> Self
    where
        I: Iterator<Item = &'a ZZ>,
    {
        iter.fold(zz!(1), |acc, zz| ZZ{ v: &acc.v * &zz.v })
    }
}


impl_self_ref_comb!(ZZ, *, Mul, mul);

macro_rules! impl_mul {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, *, Mul, mul, $type);
            impl_rhs_ref_comb!(ZZ, *, Mul, mul, $type);

        )*
    }
}
impl_mul!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, *=, MulAssign, mul_assign);

macro_rules! impl_mul_assign {
    ($($type:ident),*) => {
        $(
            impl_rhs_ref_comb_assign!(ZZ, *=, MulAssign, mul_assign, $type);
        )*
    }
}
impl_mul_assign!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

#[cfg(test)]
mod test {
    use crate::unit::zz::{zz, ZZ};

    #[test]
    fn basic_mul() {
        let v: Vec<i32> = [-2, -1, 0, 1, 2, 221, 361].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = ZZ::from(t1) * ZZ::from(t2);
                assert_eq!(a, (t1 * t2));
            }
        }

        assert_eq!(
            zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                * zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(8895043429241668574434907532615352178143049964713237064559465241187884298362511346603759790271146686520555554516587524839603911746592885667275628376783)
        );
    }

    #[test]
    fn basic_mul_ref() {
        let v: Vec<i32> = [-2, -1, 0, 1, 2, 213, 361].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = &ZZ::from(t1) * &ZZ::from(t2);
                assert_eq!(a, (t1 * t2));
            }
        }

        assert_eq!(
            &zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                * &zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(8895043429241668574434907532615352178143049964713237064559465241187884298362511346603759790271146686520555554516587524839603911746592885667275628376783)
        );
    }
}
