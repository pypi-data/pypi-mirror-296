use super::ZZ;
use crate::unit::macro_util::*;
use std::ops::{BitAnd, BitAndAssign, BitOr, BitOrAssign, BitXor, BitXorAssign};
use std::ops::{Shl, Shr, ShlAssign, ShrAssign};

impl_self_ref_comb!(ZZ, &, BitAnd, bitand);

macro_rules! impl_and {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, &, BitAnd, bitand, $type);
            impl_rhs_ref_comb!(ZZ, &, BitAnd, bitand, $type);

        )*
    }
}
impl_and!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, &=, BitAndAssign, bitand_assign);

impl_self_ref_comb!(ZZ, |, BitOr, bitor);

macro_rules! impl_or {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, |, BitOr, bitor, $type);
            impl_rhs_ref_comb!(ZZ, |, BitOr, bitor, $type);

        )*
    }
}
impl_or!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, |=, BitOrAssign, bitor_assign);

impl_self_ref_comb!(ZZ, ^, BitXor, bitxor);

macro_rules! impl_xor {
    ($($type:ident),*) => {
        $(
            impl_lhs_ref_comb!(ZZ, ^, BitXor, bitxor, $type);
            impl_rhs_ref_comb!(ZZ, ^, BitXor, bitxor, $type);

        )*
    }
}
impl_xor!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);

impl_self_ref_comb_assign!(ZZ, ^=, BitXorAssign, bitxor_assign);

/*
impl Shl<ZZ> for &ZZ {
    type Output = ZZ;

    fn shl(self, rhs: ZZ) -> Self::Output {
        ZZ {
            v: &self.v << &rhs.v,
        }
    }
}

impl Shr<ZZ> for &ZZ {
    type Output = ZZ;

    fn shr(self, rhs: ZZ) -> Self::Output {
        ZZ {
            v: &self.v >> rhs.v,
        }
    }
}
*/

macro_rules! impl_bit_operator {
    ($($type:ident),*) => {
        $(
            impl Shl<$type> for ZZ {
                type Output = ZZ;

                fn shl(self, rhs: $type) -> Self::Output {
                    ZZ {
                        v: &self.v << rhs,
                    }
                }
            }
            impl Shl<$type> for &ZZ {
                type Output = ZZ;

                fn shl(self, rhs: $type) -> Self::Output {
                    ZZ {
                        v: &self.v << rhs,
                    }
                }
            }
            impl ShlAssign<$type> for ZZ {
                fn shl_assign(&mut self, rhs: $type) -> () {
                    self.v <<= rhs;
                }
            }

            impl Shr<$type> for ZZ {
                type Output = ZZ;

                fn shr(self, rhs: $type) -> Self::Output {
                    ZZ {
                        v: &self.v >> rhs,
                    }
                }
            }
            impl Shr<$type> for &ZZ {
                type Output = ZZ;

                fn shr(self, rhs: $type) -> Self::Output {
                    ZZ {
                        v: &self.v >> rhs,
                    }
                }
            }
            impl ShrAssign<$type> for ZZ {
                fn shr_assign(&mut self, rhs: $type) -> () {
                    self.v >>= rhs;
                }
            }
        )*
    }
}

impl_bit_operator!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);
