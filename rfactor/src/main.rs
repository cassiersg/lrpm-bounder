
#[macro_use]
extern crate structopt;

use std::io;
use std::io::prelude::*;
use std::fs::File;
use std::collections::HashMap;
use std::str;
use std::error;
use std::fmt;
use std::iter;
use std::f64;

use std::path::{Path,PathBuf};
use structopt::StructOpt;

const INCR_TOL: f64 = 1e2*f64::EPSILON;

#[derive(StructOpt, Debug)]
#[structopt(name = "rfactor")]
struct Opt {
    /// Input file
    #[structopt(short = "i", long = "input", parse(from_os_str))]
    input: PathBuf,
    /// Precision (in bits)
    #[structopt(short="p", long="precision")]
    precision: f64,
    /// Leakage per share manipulation (MI in bits)
    #[structopt(short="l", long="leakage")]
    leakage: f64,
    /// Maximum number of iterations
    #[structopt(short="m", long="max-iter", default_value="100")]
    max_iter: u32,
    /// Number of leakage traces
    #[structopt(short="t", long="traces", default_value="1")]
    n: u32,
}

fn read_input(path: &Path) -> Result<String, io::Error> {
    let mut f = File::open(path)?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    return Ok(s);
}

#[derive(Debug,PartialEq,Eq)]
enum OpKind {
    Sum,
    Product,
}

#[derive(Debug)]
struct InvalidOpKindError {
   origin: String,
}

impl fmt::Display for InvalidOpKindError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", &self.origin)
    }
}

impl error::Error for InvalidOpKindError {
    fn description(&self) -> &str {
        &self.origin
    }
}

impl str::FromStr for OpKind {
    type Err = InvalidOpKindError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "*" => Ok(OpKind::Product),
            "+" => Ok(OpKind::Sum),
            _ => Err(InvalidOpKindError{ origin: s.to_string()}),
        }
    }
}

#[derive(Debug)]
struct FactorGraph<'a> {
    /// Map from var name to var id
    names_ids: HashMap<&'a str, usize>,
    /// Are vars continuous ?
    vars_cont: Vec<bool>,
    /// Number of leakage points for each variable
    vars_leakage: Vec<u32>,
    /// Operations: kind and operands (including result)
    ops: Vec<(OpKind, Vec<usize>)>,
    /// Number of operations linked to each variable
    nb_ops_var: Vec<usize>,
    /// For each op, and for each operand, the id for the operation
    /// wrt this operand (aka relative op id).
    /// The relative op ids unique for a given variable, but not globally
    /// the are assigned in sequential order. This allows the belief
    /// propagation to write the propagated output correctly to each variable.
    operands_op_ids: Vec<Vec<usize>>,
}

#[derive(Debug)]
struct BeliefState<'a: 'b, 'b> {
    mi_vars: Vec<f64>,
    mi_edges_to_vars: Vec<Vec<f64>>,
    factor_graph: &'b FactorGraph<'a>,
}

impl<'a> FactorGraph<'a> {
    fn new() -> FactorGraph<'a> {
        FactorGraph {
            names_ids: HashMap::new(),
            vars_cont: Vec::new(),
            vars_leakage: Vec::new(),
            ops: Vec::new(),
            nb_ops_var: Vec::new(),
            operands_op_ids: Vec::new(),
        }
    }

    fn get_var_or_insert(&mut self, name: &'a str) -> usize {
        if self.names_ids.contains_key(name) {
            *self.names_ids.get(name).unwrap()
        } else {
            let id = self.vars_cont.len();
            self.vars_cont.push(false);
            self.vars_leakage.push(0);
            self.nb_ops_var.push(0);
            self.names_ids.insert(name, id);
            id
        }
    }

    fn insert_op(&mut self, opkind: OpKind, operands: Vec<usize>) {
        let operands_op_id = operands
                .iter()
                .map(|operand| {
                    self.nb_ops_var[*operand] += 1;
                    self.nb_ops_var[*operand] - 1
                })
                .collect();
        self.operands_op_ids.push(operands_op_id);
        self.ops.push((opkind, operands))
    }

    fn insert_op_and_vars(&mut self, opkind: OpKind, operands: &[&'a str]) {
        let operands_idx: Vec<_> = operands
            .iter()
            .map(|x| self.get_var_or_insert(x))
            .collect();
        self.insert_op(opkind, operands_idx);
    }

    fn new_belief_state<'b>(&'b self) -> BeliefState<'a, 'b> {
        let mi_vars = iter::repeat(0.0).take(self.vars_cont.len()).collect();
        let mi_edges_to_vars = self.nb_ops_var
            .iter()
            .map(|nb| iter::repeat(0.0).take(*nb).collect())
            .collect();
        return BeliefState { mi_vars, mi_edges_to_vars, factor_graph: self };
    }
}

impl<'a, 'b> BeliefState<'a, 'b> {
    fn compute_vars_sums(&mut self, mi_leak: f64, n: u32) -> f64 {
        let mut max_delta = 0.0;
        for var in 0..self.factor_graph.vars_cont.len() {
            let intrinsic_leakage =
                mi_leak * (self.factor_graph.vars_leakage[var] as f64);
            let extrinsic_leakage: f64 = self.mi_edges_to_vars[var].iter().sum();
            let cont_coef = if self.factor_graph.vars_cont[var] { n } else { 1 };
            let old_mi = self.mi_vars[var];
            let new_mi = 
                (cont_coef as f64) * (intrinsic_leakage + extrinsic_leakage);
            if new_mi + INCR_TOL < old_mi {
                panic!("old_mi {} new_mi {} var {}", old_mi, new_mi, var);
            }
            self.mi_vars[var] = f64::max(old_mi, new_mi);
            let delta = (new_mi - old_mi).abs();
            max_delta = f64::max(max_delta, delta);
        }
        return max_delta;
    }

    fn clip_vars_mi(&mut self) {
        for mi in self.mi_vars.iter_mut() {
            *mi = f64::min(1.0, *mi);
        }
    }

    fn compute_ops_products(&mut self, alpha: f64, beta: f64) {
        for op in 0..self.factor_graph.ops.len() {
            let operands = &self.factor_graph.ops[op].1;
            let loss_factor = match self.factor_graph.ops[op].0 {
                OpKind::Sum => alpha,
                OpKind::Product => beta,
            }.powi((operands.len() - 2) as i32);
            let operands_op_id = &self.factor_graph.operands_op_ids[op];
            let mut new_msgs = Vec::with_capacity(operands.len());
            for dst_operand in operands.iter() {
                let new_msg: f64 = operands
                    .iter()
                    .enumerate()
                    .filter(|&(_, operand)| *operand != *dst_operand)
                    .map(|(i, operand)| {
                        let full_mi = self.mi_vars[*operand];
                        let operand_op_id = operands_op_id[i];
                        let own_mi = self.mi_edges_to_vars[*operand][operand_op_id];
                        f64::min(1.0, full_mi - own_mi)
                    })
                    .product();
                new_msgs.push(loss_factor * new_msg);
            }
            for ((i, dst_operand), new_msg) in
                operands.iter().enumerate().zip(new_msgs.iter()) {
                let old_msg = self.mi_edges_to_vars[*dst_operand][operands_op_id[i]];
                if old_msg > *new_msg + INCR_TOL {
                    panic!("old_msg {} new_msg {} op {} dst_operand {}",
                           old_msg, *new_msg, op, dst_operand);
                }
                self.mi_edges_to_vars[*dst_operand][operands_op_id[i]] = f64::max(old_msg, *new_msg);
            }
        }
    }

    fn run_belief_propagation(
        &mut self,
        mi_leak: f64,
        alpha: f64,
        beta: f64,
        n: u32,
        mi_tol: f64,
        max_iter: u32
        ) -> u32 {
        let mut max_delta = 0.0;
        for i in 0..max_iter {
            max_delta = self.compute_vars_sums(mi_leak, n);
            if max_delta < mi_tol {
                self.clip_vars_mi();
                return i;
            }
            self.compute_ops_products(alpha, beta);
        }
        panic!("Max iteration count exceeded. max_delta: {}\n {:#?}",
               max_delta, &self.mi_vars);
    }
}

fn main() {
    let opt = Opt::from_args();
    let s = read_input(&opt.input).unwrap();
    let mut graph = FactorGraph::new();
    for line in s.split('\n').filter(|x| !x.is_empty()) {
        let chunks: Vec<_> = line.split(' ').filter(|x|  !x.is_empty()).collect();
        assert!(chunks.len() >= 2);
        match chunks[0] {
            "E" => {
                assert!(chunks.len() >= 4);
                let opkind = chunks[1].parse().unwrap();
                graph.insert_op_and_vars(opkind, &chunks[2..]);
            }
            "L" => {
                assert!(chunks.len() == 3);
                let id = graph.get_var_or_insert(chunks[1]);
                graph.vars_leakage[id] = chunks[2].parse().unwrap();
            }
            "C" => {
                let id = graph.get_var_or_insert(chunks[1]);
                graph.vars_cont[id] = true;
            }
            _ => panic!("Invalid line {}", line),
        };
    }
    println!("{:#?}", graph);
    let mut bs = graph.new_belief_state();
    let nb_iter = bs.run_belief_propagation(
        opt.leakage, 1.0, 1.0, opt.n, opt.precision, opt.max_iter);
    println!("nb_iter {}", nb_iter);
    println!("{:#?}", bs.mi_vars);
}