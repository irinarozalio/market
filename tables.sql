DROP TABLE market.stocks;
DROP TABLE market.products;
DROP TABLE market.colors;
DROP TABLE market.fabric;
DROP TABLE market.locations;
DROP TABLE market.product_size;

CREATE TABLE market.colors
(
    id SERIAL,
    color_id integer NOT NULL,
    color_name character varying(40) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT colors_pkey PRIMARY KEY (color_id),
    CONSTRAINT unq_color_name UNIQUE (color_name)
);


CREATE TABLE market.fabric
(
    id SERIAL,
    fabric_id integer NOT NULL,
    fabric_name character varying(40) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT fabric_pkey PRIMARY KEY (fabric_id),
    CONSTRAINT unq_fabric_name UNIQUE (fabric_name)
);


CREATE TABLE market.locations
(
    id SERIAL,
    location_id integer NOT NULL,
    location_name character varying(80) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT locations_pkey PRIMARY KEY (location_id)
);

CREATE TABLE market.product_size
(
    id SERIAL,
    size_id integer NOT NULL,
    size_name character varying(40) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_size_id PRIMARY KEY (size_id)
);

CREATE TABLE market.products
(
    id SERIAL,
    product_id integer NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    size_id integer NOT NULL,
    color_id integer NOT NULL,
    fabric_id integer NOT NULL,
    image_url text COLLATE pg_catalog."default",
    CONSTRAINT pk_product_id PRIMARY KEY (product_id),
    CONSTRAINT fk_color_id FOREIGN KEY (color_id)
        REFERENCES market.colors (color_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_fabric_id FOREIGN KEY (fabric_id)
        REFERENCES market.fabric (fabric_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_size_id FOREIGN KEY (size_id)
        REFERENCES market.product_size (size_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE market.stocks
(
    id SERIAL,
    stocks_id integer NOT NULL,
    product_id integer NOT NULL,
    amount integer NOT NULL,
    location_id integer NOT NULL,
    CONSTRAINT stocks_pkey PRIMARY KEY (id),
    CONSTRAINT fk_location_id FOREIGN KEY (location_id)
        REFERENCES market.locations (location_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_product_id FOREIGN KEY (product_id)
        REFERENCES market.products (product_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);