SET search_path = market, public;

DROP TABLE stocks;
DROP TABLE products;
DROP TABLE colors;
DROP TABLE fabric;
DROP TABLE locations;
DROP TABLE product_size;

DROP TABLE IF EXISTS colors CASCADE;
CREATE TABLE colors
(
    color_id SERIAL PRIMARY KEY NOT NULL,
    color_name VARCHAR(45) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS fabric CASCADE;
CREATE TABLE fabric
(
    fabric_id SERIAL PRIMARY KEY NOT NULL,
    fabric_name VARCHAR(45) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS locations CASCADE;
CREATE TABLE locations
(
    location_id SERIAL PRIMARY KEY NOT NULL,
    location_name VARCHAR(45) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS product_size CASCADE;
CREATE TABLE product_size
(
    size_id SERIAL PRIMARY KEY NOT NULL,
    size_name VARCHAR(45) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products
(
    product_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    price money NOT NULL,
    size_id INT REFERENCES product_size (size_id) NOT NULL,
    color_id INT REFERENCES colors (color_id) NOT NULL,
    fabric_id INT REFERENCES fabric (fabric_id) NOT NULL,
    image bytea 
);

DROP TABLE IF EXISTS stocks CASCADE;
CREATE TABLE stocks
(
    stocks_id SERIAL PRIMARY KEY NOT NULL,
    product_id INT REFERENCES products (product_id) NOT NULL,
    amount INT NOT NULL,
    location_id INT REFERENCES locations (location_id) NOT NULL
);