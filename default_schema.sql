
CREATE TABLE product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    currency CHAR(3) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE customer (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(60),
    name VARCHAR(20),
    surname VARCHAR(20),
    address VARCHAR(60),
    email VARCHAR(50),
    card_type VARCHAR(30)
);

CREATE TABLE customer_order (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(id),
    product_id BIGINT NOT NULL REFERENCES product(id),
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency CHAR(3) NOT NULL
);
