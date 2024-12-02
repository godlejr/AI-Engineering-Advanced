# LLaVA
## Set up LLaVA Environments
- 만약, 지난 시간에 설치했던 XNNPACK 환경이 존재한다면 해당 환경을 실행시켜주십시오.
- XNNPACK 환경이 세팅되어 있지 않다면, 업로드한 `llava_env.zip` 파일을 받고 `./docker-build.sh` 명령어를 통해 XNNPACK 도커 환경을 구성해주십시오.
## Set up Executorch & LLaVA libraries
- 비어있는 `.sh` 파일을 하나 생성해주세요.
```
set -exu

TARGET_OS=${2:-Native}
BUILD_DIR=${3:-cmake-out}
CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE:-Release}

if [[ -z "${PYTHON_EXECUTABLE:-}" ]]; then
    PYTHON_EXECUTABLE=python3
fi

NPROC=8
if hash nproc &> /dev/null; then NPROC=$(nproc); fi

EXECUTORCH_COMMON_CMAKE_ARGS="                      \
        -DCMAKE_INSTALL_PREFIX=${BUILD_DIR}         \
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}            \
        -DEXECUTORCH_ENABLE_LOGGING=ON              \
        -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON      \
        -DEXECUTORCH_BUILD_EXTENSION_DATA_LOADER=ON \
        -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON      \
        -DEXECUTORCH_BUILD_KERNELS_CUSTOM=ON        \
        -DEXECUTORCH_BUILD_KERNELS_OPTIMIZED=ON     \
        -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON     \
        -DEXECUTORCH_BUILD_XNNPACK=ON               \
        -DEXECUTORCH_DO_NOT_USE_CXX11_ABI=ON        \
        -DEXECUTORCH_XNNPACK_SHARED_WORKSPACE=ON"

cmake_install_executorch_libraries() {
    cmake                               \
        ${EXECUTORCH_COMMON_CMAKE_ARGS} \
        -B${BUILD_DIR} .

    cmake --build ${BUILD_DIR} -j${NPROC} --target install --config ${CMAKE_BUILD_TYPE}
}

LLAVA_COMMON_CMAKE_ARGS="                        \
        -DPYTHON_EXECUTABLE="$PYTHON_EXECUTABLE" \
        -DCMAKE_INSTALL_PREFIX=${BUILD_DIR}      \
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}         \
        -DEXECUTORCH_BUILD_KERNELS_CUSTOM=ON     \
        -DEXECUTORCH_BUILD_KERNELS_OPTIMIZED=ON  \
        -DEXECUTORCH_BUILD_XNNPACK=ON"

cmake_build_llava_runner() {
    dir=examples/models/llava
    python_lib=$($PYTHON_EXECUTABLE -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')

    cmake                                 \
        ${LLAVA_COMMON_CMAKE_ARGS}        \
        -DCMAKE_PREFIX_PATH="$python_lib" \
        -B${BUILD_DIR}/${dir}             \
        ${dir}

    cmake --build ${BUILD_DIR}/${dir} -j${NPROC} --config ${CMAKE_BUILD_TYPE}
}

cmake_install_executorch_libraries
cmake_build_llava_runner
```
- 파일 실행 권환 설정과 함께 실행해주세요. `<>` 사이에 만드신 파일 이름을 넣으시면 됩니다.
```
chmod 777 <llava_x86_setup.sh>
./<llava_x86_setup.sh>
```

## Export Model & Tokenizer & Image 
```
python -m examples.models.llava.export_llava --pte-name llava.pte --with-artifacts
```
- 만약, 다른 이미지를 테스트하길 원하신다면 아래 명령어를 수행하시면 됩니다.
```
python -m examples.models.llava.image_util --image-path <basketball.jpg> --output-path image.pt
```
## 여기서부터는 로컬 Executorch 환경이 필요합니다.
## Build Android Demo App
### Build AAR Library
```
export ANDROID_ABI=arm64-v8a
export ANDROID_NDK=/opt/android-sdk/ndk/26.3.11579264
```
### Push Model, Tokenizer and Example image
```
adb push llava.pte /data/local/tmp/llama/
adb push tokenizer.bin /data/local/tmp/llama/
adb push image.pt /data/local/tmp/llama/
```
### Build Android Java Extension Code
```
pushd extension/android
./gradlew build
popd
```
### Run the following command set up the required JNI library
```
pushd examples/demo-apps/android/LlamaDemo
./gradlew :app:setup
popd
```
### Run the Android Demo App
```
export ANDROID_HOME=/opt/android-sdk
pushd examples/demo-apps/android/LlamaDemo
./gradlew :app:installDebug
popd
```