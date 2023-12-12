from llama_cpp import Llama
from os import open, write

llm = Llama(model_path="./llama.cpp/models/7B/ggml-model-q4_0.bin")

output = llm(
    "Q: Name the planets in the solar system? A: ", # Prompt
    max_tokens=32, # Generate up to 32 tokens
    stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
    echo=True # Echo the prompt back in the output
) # Generate a completion, can also call create_completion
print()
print("Output 0:")
print(output)

for i in range(3):
    output = llm(
        "Q: What are the names of the planets in the solar system in order from closest to farthest from the Sun? A: ",
        max_tokens=256,
        stop=["Q:", "\n"],
        echo=False
    )
    print()
    print(f"Output 1.{i}:")
    print(output)

for i in range(3):
    output = llm(
        """Q: Create a JSON array containing 10 JSON object representing realistic products to be imported in this SQL table:
    CREATE TABLE product (
        id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, currency CHAR(3) NOT NULL, price DECIMAL(10,2) NOT NULL
    ) .
    The name column must contain precise names of a manufacturer and model.
    The currency column must contain the ISO 4217 3-letter code of a currency.
    Return only the JSON array. A: """,
        max_tokens=2048,
        stop=["Q:"],
        echo=False
    )
    print()
    print(f"Output 2.{i}:")
    print(output)
    with open(f"output.2.{i}.json", "wt") as file:
        write(file, output.encode("utf-8"))
