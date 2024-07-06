# DVC Get Started: Experiments

This is a Computer Vision (CV) project that solves the problem of segmenting out
swimming pools from satellite images. It is based on the auto-generated [repository](https://github.com/iterative/example-get-started-experiments) for [Get Started: Experiments](https://dvc.org/doc/start/experiment-management) which demonstartes how [DVC](https://dvc.org) can be used in machine learning experiment tracking.

[Example results](./results/evaluate/plots/images/)

We use a slightly modified version of the [BH-Pools dataset](http://patreo.dcc.ufmg.br/2020/07/29/bh-pools-watertanks-datasets/):
we split the original 4k images into tiles of 1024x1024 pixels.

## Installation

Python 3.8+ is required to run code from this repo.

```console
$ git clone https://github.com/PreciousTosin/example-get-started-experiments.git
$ cd example-get-started-experiments
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/) or [conda environment](https://docs.anaconda.com/working-with-conda/environments/) Conda is prefereable if it is installed:

### Conda

```console
$ conda info --envs (view environments)
$ conda create -n <ENV_NAME>
$ conda activate <ENV_NAME>
$ pip install -r requirements.txt
```

Or if you want to use the conda `environment.yml` file in this repo:

```console
$ conda env create -f environment.yml
$ conda activate <ENV_NAME>
$ pip install -r requirements.txt
```

### Virtualenv

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Data Remote Storage

This DVC project comes with a preconfigured DVC
[remote storage](https://dvc.org/doc/commands-reference/remote) that holds raw
data (input), intermediate, and final results that are produced.

```console
$ dvc remote list
gdrive-remote   gdrive://1Ue10yGRbWC3gN9mMdCz6QhLv33wne8tq/example-get-started-experiments
```

You can run [`dvc pull`](https://man.dvc.org/pull) to download the data:

```console
$ dvc pull
```

## Running in your environment

Run [`dvc exp run`](https://man.dvc.org/exp/run) to reproduce the
[pipeline](https://dvc.org/doc/user-guide/pipelines/defining-pipelinese):

```console
$ dvc exp run
Data and pipelines are up to date.
```

If you'd like to test commands like [`dvc push`](https://man.dvc.org/push),
that require write access to the remote storage, the easiest way would be to set
up a "local remote" on your file system:

> This kind of remote is located in the local file system, but is external to
> the DVC project.

```console
$ mkdir -p /tmp/dvc-storage
$ dvc remote add local /tmp/dvc-storage
```

You should now be able to run:

```console
$ dvc push -r local
```

## Existing stages

There is a couple of git tags in this project :

### [1-notebook-dvclive](https://github.com/iterative/example-get-started-experiments/tree/1-notebook-dvclive)

Contains an end-to-end Jupyter notebook that loads data, trains a model and
reports model performance.
[DVCLive](https://dvc.org/doc/dvclive) is used for experiment tracking.
See this [blog post](https://iterative.ai/blog/exp-tracking-dvc-python) for more
details.

### [2-dvc-pipeline](https://github.com/iterative/example-get-started-experiments/tree/2-dvc-pipeline)

Contains a DVC pipeline `dvc.yaml` that was created by refactoring the above
notebook into individual pipeline stages.

The pipeline artifacts (processed data, model file, etc) are automatically
versioned.

This tag also contains a GitHub Actions workflow that reruns the pipeline if any
changes are introduced to the pipeline-related files.
[CML](https://cml.dev/) is used in this workflow to provision a cloud-based GPU
machine as well as report model performance results in Pull Requests.

## Model Deployment

Check out the [GitHub Workflow](https://github.com/iterative/example-get-started-experiments/blob/main/.github/workflows/deploy-model.yml)
that uses the [Iterative Studio Model Registry](https://dvc.org/doc/studio/user-guide/model-registry/what-is-a-model-registry).
to deploy the model to [AWS Sagemaker](https://aws.amazon.com/es/sagemaker/) whenever a new [version is registered](https://dvc.org/doc/studio/user-guide/model-registry/register-version).

## Project structure

The data files, DVC files, and results change as stages are created one by one.
After cloning and using [`dvc pull`](https://man.dvc.org/pull) to download
data, models, and plots tracked by DVC, the workspace should look like this:

```console
$ tree -L 2
.
├── LICENSE
├── README.md
├── data.            # <-- Directory with raw and intermediate data
│   ├── pool_data    # <-- Raw image data
│   ├── pool_data.dvc # <-- .dvc file - a placeholder/pointer to raw data
│   ├── test_data    # <-- Processed test data
│   └── train_data   # <-- Processed train data
├── dvc.lock
├── dvc.yaml         # <-- DVC pipeline file
├── models
│   └── model.pkl    # <-- Trained model file
├── notebooks
│   └── TrainSegModel.ipynb # <-- Initial notebook (refactored into `dvc.yaml`)
├── params.yaml      # <-- Parameters file
├── requirements.txt # <-- Python dependencies needed in the project
├── results          # <-- DVCLive reports and plots
│   ├── evaluate
│   └── train
└── src              # <-- Source code to run the pipeline stages
    ├── data_split.py
    ├── evaluate.py
    └── train.py
```
