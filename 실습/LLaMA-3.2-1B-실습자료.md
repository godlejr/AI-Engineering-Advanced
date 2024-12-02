# Executorch Llama-3.2-1B 
## Setup
Just Follow up our docker file.
```
chmod 777 docker-build.sh
./docker-build.sh
```

## Download Llama-3.2-1B-Instruct Model
Prepare Huggingface ID & Tokens
```
cd / && source llama/llama-env/bin/activate
huggingface-cli login
git-lfs install
git config --global lfs.largefilewarning false
```
```
cd /executorch
git clone https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
```
And then, you can find the model checkpoint, params.json and tokenizer.model in **Llama-3.2-1B-Instruct/original** folder.
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/qairt/2.26.0.240828/lib/x86_64-linux-clang/
```

## Export 
At the first, we register the model path as an env path 
```
export MODEL_DIR=Llama-3.2-1B-Instruct/original
```
- **[NORMAL]** If you just want to export the model using the QNN backend, use the following command. {: style="text-align: justify;"}
  ```
  python -m examples.models.llama.export_llama -kv --disable_dynamic_shape --qnn -d fp32 -c ${MODEL_DIR}/consolidated.00.pth -p ${MODEL_DIR}/params.json
  ```
- **[QUANTIZE]** Next, we will quantize and export the model using QNN Quantizer. Executorch provides a total of 3 QNN Quantizers.
  - USE: 16a16w
    ```
    python -m examples.models.llama.export_llama --checkpoint "${MODEL_DIR}/consolidated.00.pth" -p "${MODEL_DIR}/params.json" -kv --disable_dynamic_shape --qnn --pt2e_quantize qnn_16a16w -d fp32 --metadata '{"get_bos_id":128000, "get_eos_ids":[128009, 128001]}' --output_name="llama32_qnn_16a16w.pte"
    ```
  - USE: 8a8w
    ```
    python -m examples.models.llama.export_llama --checkpoint "${MODEL_DIR}/consolidated.00.pth" -p "${MODEL_DIR}/params.json" -kv --disable_dynamic_shape --qnn --pt2e_quantize qnn_8a8w -d fp32 --metadata '{"get_bos_id":128000, "get_eos_ids":[128009, 128001]}' --output_name="llama32_qnn_8a8w.pte"
    ```
  - USE: 16a4w  
    ```
    python -m examples.models.llama.export_llama --checkpoint "${MODEL_DIR}/consolidated.00.pth" -p "${MODEL_DIR}/params.json" -kv --disable_dynamic_shape --qnn --pt2e_quantize qnn_16a4w -d fp32 --metadata '{"get_bos_id":128000, "get_eos_ids":[128009, 128001]}' --output_name="llama32_qnn_16a4w.pte"
    ```
- **[CALIBRATION]** During the model quantization process, a calibration step may be required. Ensure that the prompt template includes the special tokens of the model during the calibration process.
  ```
  python -m examples.models.llama.export_llama  -t ${MODEL_DIR}/tokenizer.model -p ${MODEL_DIR}/params.json -c ${MODEL_DIR}/consolidated.00.pth  --use_kv_cache  --qnn --pt2e_quantize qnn_16a16w --disable_dynamic_shape --calibration_tasks wikitext --calibration_limit 1 --calibration_seq_length 128  --calibration_data "<|start_header_id|>system<|end_header_id|>\n\nYou are a funny chatbot.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nCould you tell me about Facebook?<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n" --metadata '{"get_bos_id":128000, "get_eos_ids":[128009, 128001]}' --output_name="llama32_qnn_cal_16a16w.pte"
  ```

# Test on your Device
## Upload QNN backend .so files
```
adb push cmake-android-out/lib/libqnn_executorch_backend.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtp.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnSystem.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV69Stub.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV73Stub.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV75Stub.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/hexagon-v69/unsigned/libQnnHtpV69Skel.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/hexagon-v73/unsigned/libQnnHtpV73Skel.so /data/local/tmp/llama/
adb push ${QNN_SDK_ROOT}/lib/hexagon-v75/unsigned/libQnnHtpV75Skel.so /data/local/tmp/llama/
```
 
## Upload Model and Tokenizer
```
adb push llama32_qnn_16a16w.pte /data/local/tmp/llama
adb push tokenizer.model /data/local/tmp/llama
adb push cmake-out-android/examples/models/llama/llama_main /data/local/tmp/llama
```

### Connecting with Android and Hexagon dynamic linkers through Library PATH
```
export LD_LIBRARY_PATH=/data/local/tmp/llama/ && export ADSP_LIBRARY_PATH=/data/local/tmp/llama/
```
### Now, You can try to run the model on your device
```
adb shell

cd /data/local/tmp/llama

chmod 777 llama_main

./llama_main --model_path llama32_qnn_16a16w.pte --tokenizer_path tokenizer.model --prompt "<|start_header_id|>system<|end_header_id|>\n\nYou are a funny chatbot.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nCould you tell me about Facebook?<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
```

