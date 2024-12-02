docker buildx build . -t llama:qnn \
        --build-arg QCOM_ZIP_FILE="v2.26.0.240828.zip"\
        --build-arg QNN_VERSION="2.26.0.240828"\
        -o type=docker