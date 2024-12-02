# Executorch Basic Environments
### Update and Install Basic Dependencies
```
apt-get update
apt install -y git build-essential cmake libideep-dev python3 python3-pip vim sudo python3-venv wget unzip zsh tmux git-lfs
apt install -y unzip zip curl libc++-dev
```
### Clone Executorch Repo
```
cd / && git clone https://github.com/pytorch/executorch.git 
```
### Checkout Specific Executorch Version and Initialize Submodules
```
cd /executorch && git submodule update --init --recursive
cd /executorch && git checkout 545535
```
### Setup Python Virtual Environments
```
cd / && mkdir llama && cd llama
cd /llama && python3 -m venv llama-env
source /llama/llama-env/bin/activate && source /executorch/install_requirements.sh 
```
### Download and Install Android SDK Command Line Tools
```
cd /root && wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && unzip ./commandlinetools-linux-11076708_latest.zip
```
### Install Required JDK and Android SDK Components
```
apt install -y zip openjdk-17-jdk 
cd /root/cmdline-tools && ./bin/sdkmanager --list --sdk_root=/opt/android-sdk
cd /root/cmdline-tools &&  yes |./bin/sdkmanager "platform-tools" "ndk;26.3.11579264" --sdk_root=/opt/android-sdk
cd /root/cmdline-tools && yes | ./bin/sdkmanager "platforms;android-34"  --sdk_root=/opt/android-sdk
cd /root/cmdline-tools && yes | ./bin/sdkmanager --licenses --sdk_root=/opt/android-sdk
```
