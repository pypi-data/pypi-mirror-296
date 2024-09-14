use super::zz;
use num::bigint::BigInt;
use pyo3::prelude::*;

pub fn py_zz(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ZZ>()?;
    Ok(())
}

fn pyany_to_zz(value: &Bound<'_, PyAny>) -> PyResult<crate::ZZ> {
    if value.is_instance_of::<ZZ>() {
        let value: ZZ = value.extract()?;
        return Ok(value.v);
    }
    else {
        let value: BigInt = value.extract()?;
        let value: crate::ZZ = value.into();
        return Ok(value);
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct ZZ {
    pub(crate) v: zz::ZZ,
}

#[pymethods]
impl ZZ {
    #[new]
    fn new(num: BigInt) -> Self {
        ZZ { v: num.into() }
    }

    fn __add__(&self, rhs: Bound<'_, PyAny>) -> Self {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ addition");
        ZZ {
            v: &self.v + &rhs,
        }
    }
    fn __iadd__(&mut self, rhs: Bound<'_, PyAny>) -> () {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ addition");
        self.v += &rhs;
    }
    fn __sub__(&self, rhs: Bound<'_, PyAny>) -> Self {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ subtraction");
        ZZ {
            v: &self.v - &rhs,
        }
    }
    fn __isub__(&mut self, rhs: Bound<'_, PyAny>) -> () {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ subtraction");
        self.v -= &rhs;
    }
    fn __neg__(&self) -> Self {
        ZZ { v: -&self.v }
    }
    fn __abs__(&self) -> Self {
        ZZ {
            v: self.v.clone().abs(),
        }
    }
    fn __mul__(&self, rhs: Bound<'_, PyAny>) -> Self {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ multiplication");
        ZZ {
            v: &self.v * &rhs,
        }
    }
    fn __imul__(&mut self, rhs: Bound<'_, PyAny>) -> () {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ multiplication");
        self.v *= &rhs;
    }
    fn __truediv__(&self, rhs: Bound<'_, PyAny>) -> Self {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ division");
        ZZ {
            v: &self.v / &rhs,
        }
    }
    fn __itruediv_(&mut self, rhs: Bound<'_, PyAny>) -> () {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ division");
        self.v /= &rhs;
    }
    fn __mod__(&self, rhs: Bound<'_, PyAny>) -> Self {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ remainder");
        ZZ {
            v: &self.v % &rhs,
        }
    }
    fn __imod__(&mut self, rhs: Bound<'_, PyAny>) -> () {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ remainder");
        self.v %= &rhs;
    }

    fn __pow__(&self, exp: Bound<'_, PyAny>, modulo: Option<Bound<'_, PyAny>>) -> Self {
        if let Some(modulo) = modulo {
            let exp = pyany_to_zz(&exp).expect("wrong type for ZZ exponent");
            let modulo = pyany_to_zz(&modulo).expect("wrong type for ZZ modulus");
            ZZ { v: self.v.mod_pow(exp, modulo) }
        }
        else {
            let exp = pyany_to_zz(&exp).expect("wrong type for ZZ exponent");
            ZZ { v: self.v.pow(exp) }
        }
    }
    fn __ipow__(&mut self, exp: Bound<'_, PyAny>, modulo: Option<Bound<'_, PyAny>>) -> () {
        if let Some(modulo) = modulo {
            let exp = pyany_to_zz(&exp).expect("wrong type for ZZ exponent");
            let modulo = pyany_to_zz(&modulo).expect("wrong type for ZZ modulus");
            self.v = self.v.mod_pow(exp, modulo);
        }
        else {
            let exp = pyany_to_zz(&exp).expect("wrong type for ZZ exponent");
            self.v = self.v.pow(exp);
        }
    }

    fn __lt__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v < rhs
    }
    fn __le__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v <= rhs
    }
    fn __eq__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v == rhs
    }
    fn __ne__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v != rhs
    }
    fn __gt__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v > rhs
    }
    fn __ge__(&self, rhs: Bound<'_, PyAny>) -> bool {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ compare");
        self.v >= rhs
    }

    fn __and__(&self, rhs: Bound<'_, PyAny>) -> ZZ {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ and");
        ZZ {
            v: &self.v & &rhs,
        }
    }
    fn __or__(&self, rhs: Bound<'_, PyAny>) -> ZZ {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ or");
        ZZ {
            v: &self.v | &rhs,
        }
    }
    fn __xor__(&self, rhs: Bound<'_, PyAny>) -> ZZ {
        let rhs = pyany_to_zz(&rhs).expect("Wrong type for ZZ xor");
        ZZ {
            v: &self.v ^ &rhs,
        }
    }

    fn __lshift__(&self, rhs: u32) -> ZZ {
        ZZ { v: &self.v << rhs }
    }
    fn __rshift__(&self, rhs: u32) -> ZZ {
        ZZ { v: &self.v >> rhs }
    }

    fn __str__(&self) -> String {
        self.v.to_string()
    }
    fn __repr__(&self) -> String {
        self.v.to_string()
    }
    fn __int__(&self) -> BigInt {
        self.v.clone().into()
    }
}
