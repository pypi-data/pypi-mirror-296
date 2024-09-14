use super::ZZ;
use std::cmp::Ordering;

impl PartialEq for ZZ {
    fn eq(&self, rhs: &Self) -> bool {
        self.v == rhs.v
    }
}
impl Eq for ZZ {}


impl PartialOrd for ZZ {
    fn partial_cmp(&self, rhs: &Self) -> Option<Ordering> {
        self.v.partial_cmp(&rhs.v)
    }
}
impl Ord for ZZ {
    fn cmp(&self, rhs: &Self) -> Ordering {
        self.v.cmp(&rhs.v)
    }
}

macro_rules! impl_compare {
    ($($type:ident),*) => {
        $(
            impl PartialEq<ZZ> for $type {
                fn eq(&self, rhs: &ZZ) -> bool {
                    &ZZ::from(*self) == rhs
                }
            }
            impl PartialEq<&ZZ> for $type {
                fn eq(&self, rhs: &&ZZ) -> bool {
                    &ZZ::from(*self) == *rhs
                }
            }
            impl PartialEq<$type> for ZZ {
                fn eq(&self, rhs: &$type) -> bool {
                     self == &ZZ::from(*rhs)
                }
            }
            impl PartialEq<$type> for &ZZ {
                fn eq(&self, rhs: &$type) -> bool {
                     self == &&ZZ::from(*rhs)
                }
            }

            impl PartialOrd<ZZ> for $type {
                fn partial_cmp(&self, rhs: &ZZ) -> Option<Ordering> {
                    ZZ::from(*self).partial_cmp(rhs)
                }
            }
            impl PartialOrd<&ZZ> for $type {
                fn partial_cmp(&self, rhs: &&ZZ) -> Option<Ordering> {
                    ZZ::from(*self).partial_cmp(*rhs)
                }
            }
            impl PartialOrd<$type> for ZZ {
                fn partial_cmp(&self, rhs: &$type) -> Option<Ordering> {
                    self.partial_cmp(&ZZ::from(*rhs))
                }
            }
            impl PartialOrd<$type> for &ZZ {
                fn partial_cmp(&self, rhs: &$type) -> Option<Ordering> {
                    (*self).partial_cmp(&ZZ::from(*rhs))
                }
            }
        )*
    }
}

impl_compare!(isize, i8, i16, i32, i64, i128, usize, u8, u16, u32, u64, u128);
