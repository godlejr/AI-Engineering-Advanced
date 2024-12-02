
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
RUN source /llama/llama-env/bin/activate && pip install torchao


# Install unzip again just to make sure it's available
RUN apt update
RUN apt install -y unzip zip curl libc++-dev

# Download and install Android SDK command line tools
RUN cd /root && wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && unzip ./commandlinetools-linux-11076708_latest.zip
RUN ls /root

# Install required JDK and Android SDK components
RUN apt install -y zip openjdk-17-jdk 
RUN cd /root/cmdline-tools && ./bin/sdkmanager --list --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools &&  yes |./bin/sdkmanager "platform-tools" "ndk;26.3.11579264" --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools && yes | ./bin/sdkmanager "platforms;android-34"  --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools && yes | ./bin/sdkmanager --licenses --sdk_root=/opt/android-sdk

# Set environment variables to enable easy use of QNN

#Install rust 
#RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

#ENV PATH="/root/.cargo/bin:${PATH}"

#COPY ./llama-main-build.sh /executorch 

#RUN source /llama/llama-env/bin/activate && cd /executorch && source /executorch/llama-main-build.sh

#COPY ./llama-main-android-build.sh /executorch 

#RUN source /llama/llama-env/bin/activate && cd /executorch && source /executorch/llama-main-android-build.sh
