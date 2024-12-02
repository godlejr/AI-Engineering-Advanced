import torch
import sentencepiece as spm
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

# Story110M Checkpoint use the Llama-2-7b-hf Model
model_name = "meta-llama/Llama-2-7b-hf"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Using Tokenizer.model
# tokenizer = "your_tokenizer_path/tokenzier.model"
# tokenizer = '/home/jovyan/story110m/tokenizer.model'
# sp = spm.SentencePieceProcessor()
# sp.load(tokenizer)
# input_text = 'Once upon a time in a distant galaxy,'
# input_ids = sp.encode(input_text, out_type=int)
# inputs = torch.tensor([input_ids])

# Checkpoint load
checkpoint_path = "your_checkpoint_path/stories110M.pt"
checkpoint = torch.load(checkpoint_path, map_location="cpu")

# Model Weight Update with Checkpoint
model.load_state_dict(checkpoint, strict=False)

# Make Input Token
input_text = "Once upon a time in a distant galaxy,"  
inputs = tokenizer(input_text, return_tensors="pt")

model.eval()  # Inference Mode
with torch.no_grad():
    # AutoTokenizer Model
    outputs = model.generate(inputs["input_ids"], max_length=128)
    # SentencePiece Tokenizer Version
    # outputs = model.generate(inputs, max_length=129)

# SentencePiece Tokenizer Output Decoding
# output_ids = outputs[0].tolist()
# output_text = sp.decode(output_ids)

# AutoTokenizer Output Decoding
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Generated text:")
print(output_text)
