use super::ZZ;
use crate::unit::macro_util::*;
use std::ops::{Add, AddAssign};

impl_self_ref_comb!(ZZ, +, Add, add);

macro_rules! impl_add {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, +, Add, add, $type);
            impl_rhs_ref_comb!(ZZ, +, Add, add, $type);

        )*
    }
}
impl_add!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, +=, AddAssign, add_assign);

macro_rules! impl_add_assign {
    ($($type:ident),*) => {
        $(
            impl_rhs_ref_comb_assign!(ZZ, +=, AddAssign, add_assign, $type);
        )*
    }
}
impl_add_assign!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

#[cfg(test)]
mod test {
    use crate::unit::zz::{zz, ZZ};

    #[test]
    fn basic_add() {
        let v: Vec<i32> = [-2, -1, 0, 1, 2, 21302183, 3612321].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = ZZ::from(t1) + ZZ::from(t2);
                assert_eq!(a, t1 + t2);

                let a: ZZ = &ZZ::from(t1) + ZZ::from(t2);
                assert_eq!(a, t1 + t2);

                let a: ZZ = ZZ::from(t1) + &ZZ::from(t2);
                assert_eq!(a, t1 + t2);

                let a: ZZ = &ZZ::from(t1) + &ZZ::from(t2);
                assert_eq!(a, t1 + t2);

                let a: ZZ = ZZ::from(t1) + t2;
                assert_eq!(a, t1 + t2);

                let a: ZZ = t1 + ZZ::from(t2);
                assert_eq!(a, t1 + t2);
            }
        }

        assert_eq!(
            zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                + zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(10740399264737532395493025049862644674794011868961999659868590551762806084824)
        );
    }
}
