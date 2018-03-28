
#[macro_use]
extern crate structopt;

use std::io;
use std::io::prelude::*;
use std::fs::File;

use std::path::{Path,PathBuf};
use structopt::StructOpt;

extern crate rfactor_lib;

use rfactor_lib::FactorGraph;


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
