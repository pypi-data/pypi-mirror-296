use crate::{zz, ZZ, Error, Result};
use std::sync::Arc;

/// Montgomery curve
/// b*y^2 = x^3 + a*x + 1
#[derive(Eq, PartialEq, Clone, Debug)]
pub struct MontGomeryCurve {
    a: ZZ,
    b: ZZ,
    n: ZZ,
}

impl MontGomeryCurve  {
    pub fn new(a: ZZ, b: ZZ, n: ZZ) -> MontGomeryCurve{
        MontGomeryCurve {
            a, b, n
        }
    }
}

#[derive(PartialEq, Eq, Clone, Debug)]
pub enum Point {
    Val{ x: ZZ, y: ZZ, curve: Arc<MontGomeryCurve> },
    Inf,
}

impl Point {
    pub fn new(x: ZZ, y: ZZ, curve: Arc<MontGomeryCurve>) -> Point {
        Point::Val{ x, y, curve }
    }

    pub fn inf() -> Self {
        Point::Inf
    }

    pub fn neg(self) -> Result<Point> {
        match self {
            Point::Inf => {
                return Err(Error::NoResult);
            },
            Point::Val{x, y, curve} => {
                return Ok(Point::Val{ x, y: y.neg(), curve });
            },
        }
    }

    pub fn is_inf(&self) -> bool {
        *self == Point::Inf
    }

    pub fn add_with_diff(&self, rhs: Point, diff: &Point) -> Point {
        match (&self, &rhs, &diff) {
            (Point::Val{x:x1, y:y1, curve:curve1}, Point::Val{x:x2, y:y2, curve: curve2}, Point::Val{x:x3, y:y3, curve: curve3}) => {
                assert_eq!(curve1, curve2);
                assert_eq!(curve2, curve3);
                let u = (x1 - y1) * (x2 + y2);
                let v = (x1 + y1) * (x2 - y2);
                let add = &u + &v;
                let sub = &u - &v;
                let new_x = (y3 * &add * &add) % &curve1.n;
                let new_y = (x3 * &sub * &sub) % &curve1.n;
                return Point::new(new_x, new_y, curve1.clone());
                
            }
            _ => {
                panic!("Unable to add");
            }
        }
    }

    pub fn double(self) -> Point {
        match self {
            Point::Val{x, y, curve} => {
                let u = (&x + &y).pow(&zz!(2));
                let v = (x - y).pow(&zz!(2));
                let diff = &u - &v;
                let new_x = (&u * &v) % &curve.n;
                let tmp = (&curve.a+2) >> 2;
                let new_y = ((&v + tmp * &diff) * &diff) % &curve.n;
                return Point::new(new_x, new_y, curve.clone());
            },
            _ => {
                panic!("Unable to double");
            }
        }
    }

    pub fn product(&self, k: &ZZ) -> Point {
        let mut out = self.clone();
        let mut r = self.clone().double();
        for i in 0..k.bits() {
            if (k >> i) & 1 == 1 {
                out = r.add_with_diff(out, &self); 
                r = r.double();
            }
            else {
                r = out.add_with_diff(r, &self);
                out = out.double();
            }
        }
        return out;
    }
}


#[cfg(test)]
mod test {
    use super::{Point, MontGomeryCurve};
    use crate::{zz, ZZ};
    use std::sync::Arc;

    #[test]
    fn test_point() {
        let curve = Arc::new(MontGomeryCurve::new(zz!(1423), zz!(5123), zz!(97872)));
        let curve_c = Arc::new(MontGomeryCurve::new(zz!(1423), zz!(5123), zz!(97872)));
        let point = Point::new(zz!(129379), zz!(659742), curve.clone());
        let point_c = Point::new(zz!(129379), zz!(659742), curve_c.clone());
        assert_eq!(point, point_c);
    }
}
