from llama_cpp import Llama, LlamaGrammar
import json
import psycopg2
import sys
import re

db_connection_string = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != '' else "postgresql://postgres:postgres@localhost:5432/postgres"
model_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '' else "./llama.cpp/models/13B/ggml-model-q4_0.bin"
tries_for_each_table = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != '' else 5

print(f"Using database connection string: {db_connection_string}")
conn = psycopg2.connect(db_connection_string)

with open("./json_array.gbnf", 'r') as grammar_file:
    json_array_grammar = LlamaGrammar.from_string(grammar_file.read())

print(f"Using model: {model_path}")
llm = Llama(model_path=model_path)

with open("./initdb.d/schema.sql", 'r') as sql_file:
    full_sql = sql_file.read()

for sql_chunk in full_sql.split(";"):
    sql_chunk = sql_chunk.strip()
    if sql_chunk.startswith("CREATE TABLE"):
        print(f"SQL table statement: {sql_chunk}")
        table_name = sql_chunk.replace("CREATE TABLE","").replace("IF NOT EXISTS","").split("(")[0].strip()
        print(f"Table name: {table_name}")
        column_specs = sql_chunk.split("(",1)[1].split(",")
        valid_column_names = list(filter(
            lambda x: x != "id" and ')' not in x,
            map(lambda x: x.strip().split(" ")[0], column_specs)
        ))
        print(f"Valid column names: {valid_column_names}")

        for i in range(tries_for_each_table):
            output = llm.create_completion(
                f"Q: Create 20 realistic distinct products to be imported in a database table defined by this SQL statement: {sql_chunk}. The output must be a JSON array containing a non-empty JSON object for each product. Return only the JSON array and then stop, without returning anything else? A: ",
                max_tokens=512,
                stop=["Q:", "]"],
                grammar=json_array_grammar,
                echo=False
            )
            out_json = output["choices"][0]["text"]
            if not out_json.endswith("]"):
                out_json = out_json + "]" # Add the missing closing bracket, stripped by the python interface

            try:
                with open(f"output.{table_name}_{i}.json", 'wt') as out_file:
                    out_file.write(out_json)
            except Exception as error:
                print("Failed to write JSON output:")
                print(error)

            try:
                out_array = json.loads(out_json)  
            except Exception as error:
                print("Failed to parse JSON output:")
                print(out_json)
                print("Error:")
                print(error)
                continue
            
            try:
                for out_item in out_array:
                    print(out_item)
                    if type(out_item) == str:
                        print("The model added a JSON encoded string to the JSON array instead of an JSON object, parsing it")
                        try:
                            out_item = json.loads(out_item)
                        except:
                            print("Failed to parse JSON item:")
                            print(out_item)
                            continue
                    if type(out_item) != dict:
                        print("The model added a non-JSON-object to the JSON array, skipping it")
                        print(out_item)
                        continue
                    if len(out_item) == 0:
                        print("The model added an empty JSON object to the JSON array, skipping it")
                        continue
                    column_names = []
                    column_values = []
                    for key in out_item:
                        print(f"  {key}: {out_item[key]}")
                        if key.startswith("."): # Sometimes the model hallucinates and generates a column name starting with a dot
                            column_names = key[1:]
                        else:
                            column_name = key
                        if column_name not in valid_column_names: # Check column name to prevent SQL injection
                            print(f"  The model generated an invalid column name: {column_name}, skipping this item")
                            continue
                        column_names.append(column_name)
                        column_values.append(out_item[key])
                    
                    with conn: # https://www.psycopg.org/docs/usage.html#transactions-control
                        with conn.cursor() as cur:
                            columns = ", ".join(column_names) # Already checked to prevent SQL injection
                            placeholders = ", ".join(["%s"] * len(column_values))
                            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
                            print(f"Executing insert query: {insert_query}")
                            cur.execute(insert_query, tuple(column_values))
                            print("Insert query successfully executed")
            except Exception as error:
                print("Failed to handle JSON output:")
                print(out_json)
                print("Error:")
                print(error)

conn.close()
