
#[macro_use] extern crate cpython;

extern crate rfactor_lib;

use cpython::{PyResult, Python, PyTuple, ToPyObject};

use rfactor_lib::parse_factor;

py_module_initializer!(librfactor_python, initlibrfactor_python, PyInit_librfactor_python, |py, m| {
    try!(m.add(py, "__doc__", "This module is implemented in Rust."));
    try!(m.add(py,
               "factor_mi",
               py_fn!(
                   py,
                   factor_mi(
                       factor: &str,
                       leakage: f64,
                       n_cont: u32,
                       precision: f64,
                       max_iter: u32
                       )
                   )
               )
         );
    Ok(())
});

fn factor_mi<'a>(
    py: Python,
    factor: &'a str,
    leakage: f64,
    n_cont: u32,
    precision: f64,
    max_iter: u32
    ) -> PyResult<PyTuple> {
    let graph = parse_factor(factor);
    let res = graph.belief_prop(
        leakage, 1.0, 1.0, n_cont, precision, max_iter
        );
    Ok(res.to_py_object(py))
}

