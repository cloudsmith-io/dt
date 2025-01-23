#! /usr/bin/env bash

# Welcome!
sudo cp .devcontainer/welcome.txt /usr/local/etc/vscode-dev-containers/first-run-notice.txt

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Install Dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks

. .venv/bin/activate
