
FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

# Update and install basic dependencies
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Asia/Seoul apt install -y tzdata
RUN apt install -y git build-essential cmake libideep-dev python3 python3-pip vim sudo python3-venv wget unzip zsh tmux git-lfs

# Clone the PyTorch executorch repo
RUN cd / && git clone https://github.com/pytorch/executorch.git 

# Checkout specific executorch version and initialize submodules
RUN cd /executorch && git fetch && git pull && git checkout 545535b6
RUN cd /executorch && git submodule update --init --recursive 

# Set up Python virtual environment for llama and build executorch
RUN cd / && mkdir llama && cd llama
RUN cd /llama && python3 -m venv llama-env
RUN source /llama/llama-env/bin/activate && source /executorch/install_requirements.sh --pybind xnnpack

RUN ls /executorch
RUN source /llama/llama-env/bin/activate && cd /executorch && source /executorch/examples/models/llama/install_requirements.sh

# Install unzip again just to make sure it's available
RUN apt install -y unzip zip curl libc++-dev

