macro_rules! impl_self_ref_comb {
    ($type:ident, $op:tt, $trait:ident, $func: ident) => {
        impl $trait<$type> for $type {
            type Output = $type;

            fn $func(self, rhs: $type) -> $type {
                $type {
                    v: self.v $op rhs.v,
                }
            }
        }
        impl $trait<$type> for &$type {
            type Output = $type;

            fn $func(self, rhs: $type) -> $type {
                $type {
                    v: &self.v $op rhs.v,
                }
            }
        }
        impl $trait<&$type> for $type {
            type Output = $type;

            fn $func(self, rhs: &$type) -> $type {
                $type {
                    v: self.v $op &rhs.v,
                }
            }
        }
        impl $trait<&$type> for &$type {
            type Output = $type;

            fn $func(self, rhs: &$type) -> $type {
                $type {
                    v: &self.v $op &rhs.v,
                }
            }
        }
    }
}
pub(crate) use impl_self_ref_comb;

macro_rules! impl_lhs_ref_comb {
    ($type:ident, $op:tt, $trait:ident, $func: ident, $lhs: ident) => {
        impl $trait<$type> for $lhs {
            type Output = $type;

            fn $func(self, rhs: $type) -> $type {
                $type {
                    v: ZZ::from(self).v $op rhs.v,
                }
            }
        }
        impl $trait<$type> for &$lhs {
            type Output = $type;

            fn $func(self, rhs: $type) -> $type {
                $type {
                    v: ZZ::from(*self).v $op rhs.v,
                }
            }
        }
        impl $trait<&$type> for $lhs {
            type Output = $type;

            fn $func(self, rhs: &$type) -> $type {
                $type {
                    v: ZZ::from(self).v $op &rhs.v,
                }
            }
        }
        impl $trait<&$type> for &$lhs {
            type Output = $type;

            fn $func(self, rhs: &$type) -> $type {
                $type {
                    v: &ZZ::from(*self).v $op &rhs.v,
                }
            }
        }
    }
}
pub(crate) use impl_lhs_ref_comb;

macro_rules! impl_rhs_ref_comb {
    ($type:ident, $op:tt, $trait:ident, $func: ident, $rhs: ident) => {
        impl $trait<$rhs> for $type {
            type Output = $type;

            fn $func(self, rhs: $rhs) -> $type {
                $type {
                    v: self.v $op ZZ::from(rhs).v,
                }
            }
        }
        impl $trait<$rhs> for &$type {
            type Output = $type;

            fn $func(self, rhs: $rhs) -> $type {
                $type {
                    v: &self.v $op ZZ::from(rhs).v,
                }
            }
        }
        impl $trait<&$rhs> for $type {
            type Output = $type;

            fn $func(self, rhs: &$rhs) -> $type {
                $type {
                    v: self.v $op &ZZ::from(*rhs).v,
                }
            }
        }
        impl $trait<&$rhs> for &$type {
            type Output = $type;

            fn $func(self, rhs: &$rhs) -> $type {
                $type {
                    v: &self.v $op &ZZ::from(*rhs).v,
                }
            }
        }
    }
}
pub(crate) use impl_rhs_ref_comb;

macro_rules! impl_self_ref_comb_assign {
    ($type:ident, $op:tt, $trait: ident, $func: ident) => {
        impl $trait<$type> for $type {
            fn $func(&mut self, rhs: $type) {
                self.v $op rhs.v;
            }
        }
        impl $trait<&$type> for $type{
            fn $func(&mut self, rhs: &$type) {
                self.v $op &rhs.v;
            }
        }
    }
}
pub(crate) use impl_self_ref_comb_assign;

macro_rules! impl_rhs_ref_comb_assign {
    ($type:ident, $op:tt, $trait:ident, $func: ident, $rhs: ident) => {
        impl $trait<$rhs> for $type {
            fn $func(&mut self, rhs: $rhs) {
                self.v $op rhs;
            }
        }
    }
}
pub(crate) use impl_rhs_ref_comb_assign;
