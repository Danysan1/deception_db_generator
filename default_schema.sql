
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    description VARCHAR(50),
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE customer (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20),
    name VARCHAR(20),
    surname VARCHAR(20),
    email VARCHAR(50)
);

CREATE TABLE order (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(id),
    product_id BIGINT NOT NULL REFERENCES product(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);
