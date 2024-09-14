use super::Matrix;

impl PartialEq for Matrix {
    fn eq(&self, rhs: &Self) -> bool {
        self.v == rhs.v && self.rows == rhs.rows && self.cols == rhs.cols
    }
}
impl Eq for Matrix {}
