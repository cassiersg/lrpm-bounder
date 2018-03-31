
#[macro_use] extern crate cpython;

extern crate rfactor_lib;

use cpython::{PyResult, Python, PyTuple, ToPyObject};

use rfactor_lib::{FactorGraph,OpKind,parse_factor};

py_module_initializer!(librfactor_python, initlibrfactor_python, PyInit_librfactor_python, |py, m| {
    try!(m.add(py, "__doc__", "This module is implemented in Rust."));
    try!(m.add_class::<PyFactorGraph>(py));
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


py_class!(class PyFactorGraph |py| {
    data graph: FactorGraph;
    def __new__(
        _cls,
        vars_cont: Vec<bool>,
        vars_leakage: Vec<u32>,
        ops: Vec<(u32, Vec<usize>)>
        ) -> PyResult<PyFactorGraph> {
        PyFactorGraph::create_instance(
            py,
            FactorGraph::from_vars_and_ops(vars_cont, vars_leakage, map_str_ops(ops)),
            )
    }

    def bp_mi(
        &self,
        leakage: f64,
        n_cont: u32,
        precision: f64,
        alpha: f64,
        beta: f64,
        max_iter: u32
        ) -> PyResult<PyTuple> {
        let mut bp_state = self.graph(py).new_belief_state();
        let n_iter = bp_state.run_belief_propagation(leakage, alpha, beta, n_cont, precision, max_iter);
        let res = (bp_state.mi_vars, n_iter);
        Ok(res.to_py_object(py))
    }
});


fn map_str_ops(ops: Vec<(u32, Vec<usize>)>) -> Vec<(OpKind, Vec<usize>)> {
    ops.into_iter().map(|(op_kind, operands)| ((if op_kind == 0 {"+"} else {"*"}).parse().unwrap(), operands)).collect()
}

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

