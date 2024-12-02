FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ARG QCOM_ZIP_FILE
ARG QNN_VERSION 

# Update and install basic dependencies
RUN apt update
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive TZ=Asia/Seoul apt install -y tzdata
RUN apt install -y git build-essential cmake libideep-dev python3 python3-pip vim sudo python3-venv wget unzip zsh tmux git-lfs

RUN cd / && git clone https://github.com/pytorch/executorch.git 

RUN cd /executorch && git checkout 545535 && git submodule sync && git submodule update --init

RUN cd / && mkdir llama && cd llama 
RUN cd /llama && python3 -m venv llama-env

RUN source /llama/llama-env/bin/activate && cd /executorch && ./install_requirements.sh 
RUN source /llama/llama-env/bin/activate && cd /executorch && ./examples/models/llama/install_requirements.sh

ENV QNN_SDK_ROOT=/opt/qairt/${QNN_VERSION}
ENV PATH=$QNN_SDK_ROOT/bin:$PATH
# ENV LD_LIBRARY_PATH=$QNN_ROOT/lib:$LD_LIBRARY_PATH
# ENV LD_LIBRARY_PATH=$QNN_SDK_ROOT/lib/x86-64_linux-clang:$LD_LIBRARY_PATH
ENV PYTHONPATH=$QNN_SDK_ROOT/python:$PYTHONPATH
# ENV QNN_SDK_ROOT=${QNN_ROOT}
ENV export EXECUTORCH_ROOT=/executorch
ENV ANDROID_NDK_ROOT=/opt/android-sdk/ndk/26.3.11579264
ENV ANDROID_NDK=${ANDROID_NDK_ROOT}
ENV ANDROID_ABI=arm64-v8a
RUN cd /executorch && cp schema/program.fbs exir/_serialize/program.fbs
RUN cd /executorch && cp schema/scalar_type.fbs exir/_serialize/scalar_type.fbs

RUN cd /root && wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && unzip ./commandlinetools-linux-11076708_latest.zip
RUN apt update
RUN apt install -y zip openjdk-17-jdk 
RUN cd /root/cmdline-tools && ./bin/sdkmanager --list --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools &&  yes |./bin/sdkmanager "platform-tools" "ndk;26.3.11579264" --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools && yes | ./bin/sdkmanager "platforms;android-34"  --sdk_root=/opt/android-sdk
RUN cd /root/cmdline-tools && yes | ./bin/sdkmanager --licenses --sdk_root=/opt/android-sdk

RUN apt install -y unzip zip curl libc++-dev
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
ENV PYTHONPATH=/:$PYTHONPATH

COPY ${QCOM_ZIP_FILE} /root/
RUN cd /root && unzip /root/${QCOM_ZIP_FILE} -d /opt


COPY ./qnn-build.sh /executorch
ENV QNN_SDK_ROOT=/opt/qairt/${QNN_VERSION}
ENV LD_LIBRARY_PATH=$QNN_SDK_ROOT/lib/x86_64-linux-clang:$LD_LIBRARY_PATH
ENV PYTHONPATH=$QNN_SDK_ROOT/python:$PYTHONPATH
RUN source /llama/llama-env/bin/activate && cd /executorch && ./backends/qualcomm/scripts/build.sh --release
RUN source /llama/llama-env/bin/activate && cd /executorch && bash ./qnn-build.sh

COPY ./llama-main-android.sh /executorch 
RUN source /llama/llama-env/bin/activate && cd /executorch && bash ./llama-main-android.sh



