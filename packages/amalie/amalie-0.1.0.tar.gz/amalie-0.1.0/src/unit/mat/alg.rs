use super::Matrix;
use crate::unit::zz::ZZ;
use crate::{zz, Result, Error};

impl Matrix {
    pub fn transpose(&self) -> Matrix {
        if self.rows == 1 && self.cols == 1 || self.cols == 0 { return self.clone(); }

        let mut mat = self.clone();
        for t in 0..self.rows*self.cols {
            let (i, j) = (t/self.cols, t%self.cols);
            mat.v[t] = self.v[self.rows*j + i].clone();
        }
        std::mem::swap(&mut mat.rows, &mut mat.cols);
        mat
    }

    pub fn det(&self) -> Result<ZZ> {
        if self.rows != self.cols || self.rows == 0 {
            return Err(Error::InvalidState("rows != cols || rows == 0".to_string()));
        }
        
        if self.rows == 1 { return self.get(0,0) }
        if self.rows == 2 {
            return Ok(&self.v[0] * &self.v[3] - &self.v[1] * &self.v[2]);
        }

        let mut add = zz!(0);
        for x in 0..self.rows {
            let (mut i, mut j) = (0, x);

            let mut mul = ZZ::from(1);
            for _ in 0..self.rows {
                mul *= &self.v[i * self.cols + j];
                i += 1;
                j += 1;
                if j >= self.rows {
                    j = 0;
                }
            }
            add += mul;
        }

        let mut sub = zz!(0);
        for x in 0..self.rows {
            let (mut i, mut j) = (0, self.rows - 1 - x);

            let mut mul = zz!(1);
            for _ in 0..self.rows {
                mul *= &self.v[i * self.cols + j];
                i += 1;
                j = if j == 0 { self.rows - 1 }
                    else { j - 1 }
            }
            sub -= mul;
        }
        Ok(add + sub)
    }
}

#[cfg(test)]
mod test {
    use crate::{zz, matrix, ZZ};
    use super::Matrix;

    #[test]
    fn transpose() {
        let mat: Matrix = matrix![[1]];
        let mat_t = mat.transpose();
        assert_eq!(mat, mat_t);

        let mat = matrix![[1, 2],[3, 4]];
        let mat_t = mat.transpose();
        let mat_a = matrix![[1, 3],[2, 4]];
        assert_eq!(mat_t, mat_a);
        assert_eq!(mat_t.transpose(), mat);

        let mat = matrix![[1, 2, 3],[4, 5, 6]];
        let mat_t = mat.transpose();
        assert_eq!(mat_t, matrix![[1, 4],[2, 5], [3,6]]);
    }

    #[test]
    fn det() {
        let mat = matrix![[1]]; 
        assert_eq!(mat.det().unwrap(), 1);

        let mat = matrix![[123213, 58890912], [92349089, 90980932549089909890832908]];
        assert_eq!(mat.det().unwrap(), zz!(11210033642171009628857121514236));
        
        let mat = matrix![[845987438574387, 89798798798437, 98758932847983274], [31321321312, 21, 938479827433213], [1,2932847982374982379847329847983274,0]];
        assert_eq!(mat.det().unwrap(), zz!(-2319439557016705698734121838804798042159530631553151761401634055));
    }
}
