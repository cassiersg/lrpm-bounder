# Target MI bound computation in the LRPM

This tool was built to generate results of the paper
*Towards Globally Optimized Masking:
From Low Randomness to Low Noise Rate or Probe Isolating Multiplications with Reduced
Randomness and Security against Horizontal Attacks*


## Usage

The tool is made of three parts:
* Generation of factor graphs for various gadgets (see e.g. `mul_gen.py`)
* Belief propagation algorithm (in `rfactor`)
* Scripts generating plots (`plot_*.py`)

In order to run the tools the Rust library in rfactor should first be compiled:
```sh
$ cd rfactor && cargo build --release
```

## Dependencies

The scripts have been tested only with Python 3.6
* `joblib == 0.13.0`
* `networkx == 2.2`
* `numpy == 1.15.4`
* `matplotlib == 2.1.2`
* `matplotlib2tikz == 0.6.18` (optional, for LaTeX plot export)

The library compiles on [Rust](https://rust-lang.org) stable (`1.30.1`).

## License

Distributed under the terms of the Apache License (Version 2.0).
See [LICENSE](LICENSE) for details.
