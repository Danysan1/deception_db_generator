#!/bin/bash
set -e

# git submodule update --init
# conda activate llama2

cd llama.cpp
# make

mkidr -p models/7B

python3 convert.py --outfile ./models/7B/ggml-model-f16.bin --outtype f16 ../llama/llama-2-7b-chat --vocab-dir ../llama

./quantize ./models/7B/ggml-model-f16.bin ./models/7B/ggml-model-q4_0.bin q4_0

#./main -m ./models/7B/ggml-model-q4_0.bin -n 1024 --repeat_penalty 1.0 --color -i -r "User:" -f ./prompts/chat-with-bob.txt

# ./main -m ./models/7B/ggml-model-q4_0.bin -n 2048 --color --grammar-file ./grammars/json_arr.gbnf -p '
#     You are a helpful, kind and precise assistant.
#     Create a JSON array with 5 realistic items describing products to be imported in this PostgreSQL table: 
#     CREATE TABLE product (
#         id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, currency CHAR(3) NOT NULL, price DECIMAL(10,2) NOT NULL
#     ) .
#     The name column must contain precise names of a manufacturer and model.
#     The currency column must contain the ISO 4217 3-letter code of a currency.'

./main -m ./models/7B/ggml-model-q4_0.bin -n 4096 --color --repeat_penalty 1.0 -p '
    You are a helpful, kind and precise expert in data generation, you always answer as the expert and then stop.
    Create 10 realistic products to be imported in this SQL table: 
    CREATE TABLE product (
        id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, currency CHAR(3) NOT NULL, price DECIMAL(10,2) NOT NULL
    ) .
    The name column must contain precise names of a manufacturer and model.
    The currency column must contain the ISO 4217 3-letter code of a currency.
    The output must be a JSON array containing a JSON object for each product.
    Return only the JSON array.'