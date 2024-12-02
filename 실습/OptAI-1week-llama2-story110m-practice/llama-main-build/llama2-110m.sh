#/bin/bash 

source /llama/llama-env/bin/activate


# @ /worksapce/Llama2-110m
mkdir /workspace/Llama2-110m

cp ./params.json /workspace/Llama2-110m

cd /workspace/Llama2-110m
#wget "https://huggingface.co/karpathy/tinyllamas/resolve/main/stories110M.pt"
#wget "https://raw.githubusercontent.com/karpathy/llama2.c/master/tokenizer.model"



# @ executorch directory
cd /executorch
python -m examples.models.llama.export_llama \
    -c /workspace/Llama2-110m/stories110M.pt\
    -p /workspace/Llama2-110m/params.json \
    -X \
    -kv \
    -o /workspace/Llama2-110m/

# @ executorch directory
python -m extension.llm.tokenizer.tokenizer \
       -t /workspace/Llama2-110m/tokenizer.model \
       -o llama2-story-tokenizer.bin

# adb pushsing 
#adb push /workspace/Llama2-110m/llama2-story.pte           /data/local/tmp/llama
#adb push /workspace/Llama2-110m/llama2-story-tokenizer.bin /data/local/tmp/llama


