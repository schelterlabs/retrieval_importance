You can run the HELM benchmark to get the baseline score for non-retrieval GPT-3.5 models. 

# Installation

First, you should install crfm-helm using the following instructions.

```bash
# Create a virtual environment.
# Only run this the first time.
python3 -m pip install virtualenv
python3 -m virtualenv -p python3.8 helm-venv

# Activate the virtual environment.
source helm-venv/bin/activate

# Within this virtual environment, run:
pip install crfm-helm
```

You can find the information on installation using Anaconda here:
https://crfm-helm.readthedocs.io/en/latest/installation/

# Add Credential Key
To make API calls using HELM, you should add the credentials to a `credentials.conf` file in the default environment directory `helm/prod_env/`. 

```
openaiApiKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Detailed information can be found here: https://crfm-helm.readthedocs.io/en/latest/tutorial/#using-helm-run

# Run Benchmark
First, you should edit the `run.conf` file in the directory `helm/` to run 70 relations of WikiFact. We have provided an example file in this folder. You can copy it into `helm/`.

Run the following:
```
# Run benchmark
helm-run --conf-paths run_specs.conf --suite v1 --max-eval-instances 2700

# Summarize benchmark results
helm-summarize --suite v1

# Start a web server to display benchmark results
helm-server
```
Then go to http://localhost:8000/ in your browser.