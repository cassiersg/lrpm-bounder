
#[macro_use] extern crate cpython;

mod factor_graph;

use cpython::{PyResult, PyTuple, ToPyObject};

use factor_graph::{FactorGraph,OpKind};

py_module_initializer!(librfactor_python, initlibrfactor_python, PyInit_librfactor_python, |py, m| {
    try!(m.add(py, "__doc__", "This module is implemented in Rust."));
    try!(m.add_class::<PyFactorGraph>(py));
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
        n_cont: u64,
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

