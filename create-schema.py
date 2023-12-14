from llama_cpp import Llama, LlamaGrammar
import sys

table_description = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != '' else "a person with all the details necessary to request a loan"
model_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '' else "./llama.cpp/models/13B/ggml-model-q4_0.bin"

print(f"Using model: {model_path}")
llm = Llama(model_path=model_path)

for i in range(5):
    output = llm.create_completion(
        f"Q: Create an SQL statement to create a database table that represents {table_description}. Return only the SQL statement and then stop, without returning anything else? A: ",
        max_tokens=512,
        stop=["Q:", ";"],
        echo=False
    )
    out_sql = output["choices"][0]["text"]
    print(f"SQL statement {i}:")
    print(out_sql)
    
    with open(f"./schema.{i}.sql", 'wt') as sql_file:
        sql_file.write(out_sql)