from llama_cpp import Llama, LlamaGrammar
import os

with open("./llama.cpp/grammars/json_arr.gbnf", 'r') as grammar_file:
    json_array_grammar = LlamaGrammar.from_string(grammar_file.read())

llm = Llama(model_path="./llama.cpp/models/13B/ggml-model-q4_0.bin")

output = llm.create_completion(
    "Q: Name the planets in the solar system? A: ", # Prompt
    max_tokens=32, # Generate up to 32 tokens
    stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
    echo=True # Echo the prompt back in the output
)
print()
print("Output 0:")
print(output)

for i in range(2):
    output = llm(
        "Q: What are the names of the planets in the solar system in order from closest to farthest from the Sun? A: ",
        max_tokens=64,
        stop=["Q:", "\n"],
        echo=False
    )
    print()
    print(f"Output 1.{i}:")
    print(output)

table_sql = "CREATE TABLE product ( id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL UNIQUE, currency CHAR(3) NOT NULL, price DECIMAL(10,2) NOT NULL )"
table_data_hint = "The name column must contain precise names of a manufacturer and model. The currency column must contain the ISO 4217 3-letter code of a currency."
for i in range(5):
    output = llm(
        f"Q: Create 30 realistic distinct products to be imported in a database table defined by this SQL statement: {table_sql}. {table_data_hint} The output must be a JSON array containing a JSON object for each product. Return only the JSON array and then stop, without returning anything else? A: ",
        max_tokens=512,
        stop=["Q:", "]"],
        grammar=json_array_grammar,
        echo=False
    )
    print()
    print(f"Output 2.{i}:")
    print(output)

    with open(f"output.2.{i}.json", 'wt') as out_file:
        out_file.write(output["choices"][0]["text"]+"]")

for i in range(5):
    output = llm(
        f"Q: Create a valid SQL INSERT statement with 30 realistic distinct products for a database table defined by this SQL statement: {table_sql}. {table_data_hint}. Return only the SQL statement and then stop, without returning anything else? A: ",
        max_tokens=512,
        stop=["Q:", ";"],
        echo=False
    )
    print()
    print(f"Output 3.{i}:")
    print(output)

    with open(f"output.3.{i}.sql", 'wt') as out_file:
        out_file.write(output["choices"][0]["text"]+"]")
