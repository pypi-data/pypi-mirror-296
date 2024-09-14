use crate::unit::zz::py::*;
use pyo3::{PyAny, Bound, PyResult, wrap_pyfunction, pyfunction};
use pyo3::types::PyModule;
use pyo3::prelude::{PyModuleMethods, PyAnyMethods};
use num::BigInt;

pub fn py_alg(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(gcd, m)?)?;
    m.add_function(wrap_pyfunction!(egcd, m)?)?;
    m.add_function(wrap_pyfunction!(crt, m)?)?;
    m.add_function(wrap_pyfunction!(mod_inv, m)?)?;
    m.add_function(wrap_pyfunction!(totient, m)?)?;
    m.add_function(wrap_pyfunction!(is_prime, m)?)?;
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
fn pyany_to_veczz(value: &Vec<Bound<'_, PyAny>>) -> PyResult<Vec<crate::ZZ>> {
    let mut out = Vec::with_capacity(value.len());
    for x in value {
        out.push(pyany_to_zz(x)?);
    }
    Ok(out)
}

#[pyfunction]
fn gcd(a: Bound<'_, PyAny>, b: Bound<'_, PyAny>) -> PyResult<ZZ> {
    let a = pyany_to_zz(&a)?;
    let b = pyany_to_zz(&b)?;
    let v = crate::gcd(a, b);
    Ok(ZZ{v})
}
#[pyfunction]
fn egcd(a: Bound<'_, PyAny>, b: Bound<'_, PyAny>) -> PyResult<(ZZ, ZZ, ZZ)> {
    let a = pyany_to_zz(&a)?;
    let b = pyany_to_zz(&b)?;
    let (m, a, b) = crate::egcd(a, b);
    Ok((ZZ{v:m}, ZZ{v:a}, ZZ{v:b}))
}
#[pyfunction]
fn crt(v: Vec<Bound<'_, PyAny>>, m: Vec<Bound<'_, PyAny>>) -> PyResult<(ZZ, ZZ)> {
    let v = pyany_to_veczz(&v)?;
    let m = pyany_to_veczz(&m)?;
    let (v, n) = crate::crt(v, m);
    Ok((ZZ{v}, ZZ{v: n}))
}
#[pyfunction]
fn mod_inv(g: Bound<'_, PyAny>, exp: Bound<'_, PyAny>) -> PyResult<ZZ> {
    let g = pyany_to_zz(&g)?;
    let exp = pyany_to_zz(&exp)?;
    Ok(ZZ{v: crate::mod_inv(g, exp).unwrap()})
}
#[pyfunction]
fn totient(factors: Vec<Bound<'_, PyAny>>) -> PyResult<ZZ> {
    let factors = pyany_to_veczz(&factors)?;
    Ok(ZZ{v: crate::totient(factors)})
}
#[pyfunction]
fn is_prime(n: Bound<'_, PyAny>) -> PyResult<bool> {
    let n = pyany_to_zz(&n)?;
    Ok(crate::is_prime(n))
}
#[pyfunction]
fn pollard_rho(n: Bound<'_, PyAny>) -> PyResult<ZZ> {
    let n = pyany_to_zz(&n)?;
    Ok(ZZ{ v: crate::pollard_rho(n)? })
}
