
# My Kubernetes Workshop Platform

This repo comes with everything you need to setup a fairly simple Kubernetes cluster for a workshop. Inspired by HobbyFarm from Rancher, this platform provides attendees of your workshop with their own virtual cluster, provisioned dynamically with vcluster.

Bonus point, this solution works flawlessly with baremetal Kubernetes clusters, allowing you to literally run your workshop/bootcamp out of your basement.


## Installation

### Prerequisites
```sh
# install poetry
curl -sSL https://install.python-poetry.org | python3 -
# set .venv globally
poetry config virtualenvs.in-project true
# install dependencies
poetry install
# activate virtual environment
poetry shell
```
