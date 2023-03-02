use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::types::PyDict;

use mle::types::Retrieval;

#[pyfunction]
fn learn_importance(
    py_retrievals: &PyList,
    k: usize,
    learning_rate: f64,
    num_steps: usize,
    n_jobs: usize, // TODO allow for -1
) -> PyResult<Vec<f64>> {

    let mut retrievals: Vec<Retrieval> = Vec::with_capacity(py_retrievals.len());
    let mut corpus_size: usize = 0;

    for d in py_retrievals.iter() {
        let retrieved: Vec<usize> = d.downcast::<PyDict>()?
            .get_item("retrieved").unwrap()
            .downcast::<PyList>()?.extract().unwrap();

        if *retrieved.iter().max().unwrap() > corpus_size {
            corpus_size = *retrieved.iter().max().unwrap();
        }

        let utility_contributions: Vec<f64> = d.downcast::<PyDict>()?
            .get_item("utility_contributions").unwrap()
            .downcast::<PyList>()?.extract().unwrap();

        retrievals.push(Retrieval::new(retrieved, utility_contributions));
    }

    let v = mle::mle_importance(
        retrievals,
        corpus_size + 1,
        None,
        k,
        learning_rate,
        num_steps,
        n_jobs
    );

    Ok(v)
    /*Python::with_gil(|py| {
        let v_as_py_list: PyList = (*<&PyList as Into<PyAny>>::into(PyList::new(py, v))).extract().unwrap();
        Ok(v_as_py_list)
    })*/
}

/// A Python module implemented in Rust.
#[pymodule]
fn retrieval_importance(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(learn_importance, m)?)?;
    Ok(())
}