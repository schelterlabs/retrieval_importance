# retrieval_importance

## Installation for development

 * Requires Python 3.9 and [Rust](https://www.rust-lang.org/tools/install) to be available
 
 1. Clone the repository: `git clone git@github.com:schelterlabs/retrieval_importance.git`
 1. Change to the project directory: `cd retrieval_importance`
 1. Create a virtualenv: `python3.9 -m venv venv`
 1. Activate the virtualenv `source venv/bin/activate`
 1. Install the dev dependencies with `pip install -r requirements-dev.txt`
 1. Build the project `maturin develop --release`
 
 * Optional steps:
    * Run the tests with `cargo test --release`
    * Run the benchmarks with `cargo bench`
    * Run the Python tests `python -m pytest`
    * Start jupyter with `jupyter notebook` and run the example notebooks
