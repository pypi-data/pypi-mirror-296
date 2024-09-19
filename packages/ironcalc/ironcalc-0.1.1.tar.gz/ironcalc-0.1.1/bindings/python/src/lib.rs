use pyo3::exceptions::{PyException, PyValueError};
use pyo3::{create_exception, prelude::*, wrap_pyfunction};

use ironcalc::base::Model;

use ironcalc::export::save_to_xlsx;
use ironcalc::import::load_from_xlsx;

create_exception!(_ironcalc, WorkbookError, PyException);

#[pyclass]
pub struct PyModel {
    model: Model,
}

#[pyclass]
pub struct Cell {
    #[pyo3(get, set)]
    pub row: i32,
    #[pyo3(get, set)]
    pub column: i32,
}

#[pymethods]
impl PyModel {
    // pub fn to_string(&self) -> PyResult<> {
    //     Ok(self.model.to_bytes())
    // }

    pub fn save_to_xlsx(&self, file: &str) -> PyResult<()> {
        save_to_xlsx(&self.model, file).map_err(|e| WorkbookError::new_err(e.to_string()))
    }

    pub fn test_panic(&self) -> PyResult<()> {
        panic!("This function panics for testing panic handling");
    }
}

#[pyfunction]
pub fn load_from_file(file_path: &str, locale: &str, tz: &str) -> PyModel {
    let model = load_from_xlsx(file_path, locale, tz).unwrap();
    PyModel { model }
}

#[pyfunction]
pub fn create(name: &str, locale: &str, tz: &str) -> PyModel {
    let model = Model::new_empty(name, locale, tz).unwrap();
    PyModel { model }
}

#[pyfunction]
pub fn test_panic() {
    panic!("This function panics for testing panic handling");
}

// #[pymodule]
// fn _pyroncalc(_: Python, m: &PyModule) -> PyResult<()> {
//     m.add("__version__", env!("CARGO_PKG_VERSION"))?;

//     m.add_function(wrap_pyfunction!(create, m)?).unwrap();
//     m.add_function(wrap_pyfunction!(load_from_file, m)?)
//         .unwrap();

//     m.add_function(wrap_pyfunction!(test_panic, m)?).unwrap();

//     Ok(())
// }

#[pymodule]
// fn _pyroncalc(py: Python, m: &PyModule) -> PyResult<()> {
fn _pyroncalc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add the package version to the module
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    // Add the functions to the module using the `?` operator
    m.add_function(wrap_pyfunction!(create, m)?)?;
    m.add_function(wrap_pyfunction!(load_from_file, m)?)?;
    m.add_function(wrap_pyfunction!(test_panic, m)?)?;

    Ok(())
}