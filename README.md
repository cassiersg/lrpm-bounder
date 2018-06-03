# Target MI bound computation in the LRPM

This tool was built to generate results of the paper
*Towards Globally Optimized Masking:
From Low Randomness to Low Noise Rate or Probe Isolating Multiplications with Reduced
Randomness and Security against Horizontal Attacks*
It is likely necessary to read this paper to effectively use and understand
this tool.


## Usage

The tool is made of three parts:
* Generation of factor graphs for various gadgets
* Belief propagation algorithm (in `rfactor`)
* Scripts generating plots

In order to run the tools the Rust library in rfactor should first be compiled:
```sh
$ cd rfactor && cargo build --release
```


## Dependencies

The scripts have been tested only with Python 3.6
* `matplotlib == 2.1.2`

## License

Distributed under the terms of the Apache License (Version 2.0).
See [LICENSE](LICENSE) for details.
