use super::mat::Matrix;
use crate::unit::zz::ZZ;

impl From<&Vec<Vec<ZZ>>> for Matrix {
    fn from(item: &Vec<Vec<ZZ>>) -> Self {
        if item.len() == 0 {
            return Matrix::empty();
        }
        let mut values = vec![];
        for v in item.iter() {
            for u in v.iter() {
                values.push(u.clone());
            }
        }
        Matrix {
            v: values,
            rows: item[0].len(),
            cols: item.len(),
        }
    }
}
impl From<Vec<Vec<ZZ>>> for Matrix {
    fn from(item: Vec<Vec<ZZ>>) -> Self {
        if item.len() == 0 {
            return Matrix::empty();
        }
        let mut values = vec![];
        for v in item.iter() {
            for u in v.iter() {
                values.push(u.clone());
            }
        }
        Matrix {
            v: values,
            rows: item[0].len(),
            cols: item.len(),
        }
    }
}
