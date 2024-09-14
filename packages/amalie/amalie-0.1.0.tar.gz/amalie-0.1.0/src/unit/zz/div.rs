use super::ZZ;
use crate::unit::macro_util::*;
use std::ops::{Div, DivAssign, Rem, RemAssign};

impl_self_ref_comb!(ZZ, /, Div, div);

macro_rules! impl_div {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, /, Div, div, $type);
            impl_rhs_ref_comb!(ZZ, /, Div, div, $type);

        )*
    }
}
impl_div!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, /=, DivAssign, div_assign);

macro_rules! impl_div_assign {
    ($($type:ident),*) => {
        $(
            impl_rhs_ref_comb_assign!(ZZ, /=, DivAssign, div_assign, $type);
        )*
    }
}
impl_div_assign!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb!(ZZ, %, Rem, rem);

macro_rules! impl_rem {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, %, Rem, rem, $type);
            impl_rhs_ref_comb!(ZZ, %, Rem, rem, $type);

        )*
    }
}
impl_rem!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, %=, RemAssign, rem_assign);

macro_rules! impl_rem_assign {
    ($($type:ident),*) => {
        $(
            impl_rhs_ref_comb_assign!(ZZ, %=, RemAssign, rem_assign, $type);
        )*
    }
}
impl_rem_assign!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

#[cfg(test)]
mod test {
    use crate::unit::zz::{zz, ZZ};

    #[test]
    fn basic_div() {
        let v: Vec<i32> = [-2, -1, 1, 2, 221, 361].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = ZZ::from(t1) / ZZ::from(t2);
                assert_eq!(a, (t1 / t2));
            }
        }

        assert_eq!(
            zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                / zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(10)
        );
    }

    #[test]
    fn basic_div_ref() {
        let v: Vec<i32> = [-2, -1, 1, 2, 213, 361].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = &ZZ::from(t1) / &ZZ::from(t2);
                assert_eq!(a, (t1 / t2));
            }
        }

        assert_eq!(
            &zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                / &zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(10)
        );
    }
}
