use super::unit::zz::py::py_zz;
use super::alg::py::py_alg;
use pyo3::prelude::*;
use std::process;

use crate::Error;
use pyo3::exceptions::PyRuntimeError;

impl From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        PyRuntimeError::new_err(format!("Error: {}", err))
    }
}


#[pymodule]
#[pyo3(name = "amalie")]
fn amalie(m: &Bound<'_, PyModule>) -> PyResult<()> {
    ctrlc::set_handler(move || {
        process::exit(130);
    })
    .expect("Error setting Ctrl+C handler");

    let _ = py_zz(&m);
    let _ = py_alg(&m);
    Ok(())
}
