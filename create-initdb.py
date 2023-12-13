from llama_cpp import Llama, LlamaGrammar
import os

with open("./llama.cpp/grammars/json_arr.gbnf", 'r') as grammar_file:
    json_array_grammar = LlamaGrammar.from_string(grammar_file.read())

llm = Llama(model_path="./llama.cpp/models/13B/ggml-model-q4_0.bin")

with open("./initdb.d/schema.sql", 'r') as sql_file:
    full_sql = sql_file.read()

for sql_chunk in full_sql.split(";"):
    sql_chunk = sql_chunk.strip()
    if sql_chunk.startswith("CREATE TABLE"):
        output = llm(
            f"Q: Create 20 realistic distinct products to be imported in a database table defined by this SQL statement: {sql_chunk}. The output must be a JSON array containing a JSON object for each product. Return only the JSON array and then stop, without returning anything else? A: ",
            max_tokens=1024,
            stop=["Q:", "]"],
            grammar=json_array_grammar,
            echo=False
        )
        out_json = output["choices"][0]["text"]
        if not out_json.endswith("]"):
            out_json = out_json + "]" # Add the missing closing bracket, stripped by the python interface
        print()
        print(f"Output 0:")
        print(out_json)

        with open(f"output.0.json", 'wt') as out_file:
            out_file.write(output["choices"][0]["text"]+"}")