#!/bin/bash
set -e

# git submodule update --init
# conda activate llama2

cd llama.cpp
# make

mkidr -p models/7B

python3 convert.py --outfile ./models/7B/ggml-model-f16.bin --outtype f16 ../llama/llama-2-7b-chat --vocab-dir ../llama

./quantize ./models/7B/ggml-model-f16.bin ./models/7B/ggml-model-q4_0.bin q4_0

./main -m ./models/7B/ggml-model-q4_0.bin -n 1024 --repeat_penalty 1.0 --color -i -r "User:" -f ./prompts/chat-with-bob.txt
