use crate::unit::zz::ZZ;
use crate::{Result, Error};

#[derive(Clone, Debug)]
pub struct Matrix {
    pub(super) v: Vec<ZZ>,
    pub(super) rows: usize,
    pub(super) cols: usize,
}

impl Matrix {
    pub fn new(rows: usize, cols: usize) -> Matrix {
        let values = vec![ZZ::from(0); rows * cols];
        Matrix {
            v: values,
            rows,
            cols,
        }
    }

    pub fn empty() -> Matrix {
        let values = vec![];
        Matrix {
            v: values,
            rows: 0,
            cols: 0,
        }
    }

    pub fn set(&mut self, r: usize, c: usize, val: ZZ) -> Result<()> {
        if r < self.rows && c < self.cols {
            self.v[r * self.cols + c] = val;
            return Ok(());
        } else {
            return Err(Error::InvalidInput("r or c are out of bound".to_string()));
        }
    }
    pub fn get(&self, r: usize, c: usize) -> Result<ZZ> {
        if r < self.rows && c < self.cols {
            return Ok(self.v[r * self.cols + c].clone());
        } else {
            return Err(Error::InvalidInput("r or c are out of bound".to_string()));
        }
    }
}
