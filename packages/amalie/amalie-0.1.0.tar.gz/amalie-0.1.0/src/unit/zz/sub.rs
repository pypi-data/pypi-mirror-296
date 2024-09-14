use super::ZZ;
use crate::unit::macro_util::*;
use std::ops::{Neg, Sub, SubAssign};

impl Neg for ZZ {
    type Output = Self;

    fn neg(mut self) -> Self {
        self.v = -self.v;
        self
    }
}
impl Neg for &ZZ {
    type Output = ZZ;

    fn neg(self) -> ZZ {
        ZZ { v: -&self.v }
    }
}

impl_self_ref_comb!(ZZ, -, Sub, sub);

macro_rules! impl_sub {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, -, Sub, sub, $type);
            impl_rhs_ref_comb!(ZZ, -, Sub, sub, $type);

        )*
    }
}
impl_sub!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, -=, SubAssign, sub_assign);

macro_rules! impl_sub_assign {
    ($($type:ident),*) => {
        $(
            impl_rhs_ref_comb_assign!(ZZ, -=, SubAssign, sub_assign, $type);
        )*
    }
}
impl_sub_assign!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

#[cfg(test)]
mod test {
    use crate::unit::zz::{zz, ZZ};

    #[test]
    fn basic_sub() {
        let v: Vec<i32> = [-2, -1, 0, 1, 2, 21302183, 3612321].to_vec();
        for &t1 in v.iter() {
            for &t2 in v.iter() {
                let a: ZZ = ZZ::from(t1) - ZZ::from(t2);
                assert_eq!(a, (t1 - t2));
            }
        }

        assert_eq!(
            zz!(9836070282337477847351144893364761019994856058854208233910993662739237842381)
                - zz!(904328982400054548141880156497883654799155810107791425957596889023568242443),
            zz!(8931741299937423299209264736866877365195700248746416807953396773715669599938)
        );

        let x = zz!(123);
        assert_eq!(-&x, -zz!(123));
        assert_eq!(--x, zz!(123));
    }
}
