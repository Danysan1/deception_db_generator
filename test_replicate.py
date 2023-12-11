import replicate

output = replicate.run(
  "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
  input={
    "prompt": """
        You are a helpful, kind and precise expert in data generation, you always answer as the expert and then stop.
        Create 10 realistic products to be imported in this SQL table: 
        CREATE TABLE product (
            id BIGSERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL, currency CHAR(3) NOT NULL, price DECIMAL(10,2) NOT NULL
        ) .
        The name column must contain precise names of a manufacturer and model.
        The currency column must contain the ISO 4217 3-letter code of a currency.
        The output must be a JSON array containing a JSON object for each product.
        Return only the JSON array.
    """,
    "max_new_tokens": 250
  }
)

print(output)
