TRUNCATE stocks CASCADE;
delete from stocks;
delete from products;
delete from colors;
delete from fabric;
delete from locations;
delete from product_size;
--colors
INSERT INTO colors VALUES
    (1, 'Multicolor');
INSERT INTO colors VALUES
    (2, 'Black');
INSERT INTO colors VALUES
    (3, 'Yellow');
INSERT INTO colors VALUES
    (4, 'Khaki');
INSERT INTO colors VALUES
    (5, 'Blue');
SELECT setval('colors_color_id_seq', 5, true);

--fabric
INSERT INTO fabric VALUES
    (1, 'Polyester');
INSERT INTO fabric VALUES
    (2, 'Leather');
INSERT INTO fabric VALUES
    (3, 'Cotton');
INSERT INTO fabric VALUES
    (4, 'Silk');
INSERT INTO fabric VALUES
    (5, 'Tencel');
SELECT setval('fabric_fabric_id_seq', 5, true);

--locations
INSERT INTO locations VALUES
    (1, 'Los Angeles');
INSERT INTO locations VALUES
    (2, 'Tel Aviv');
INSERT INTO locations VALUES
    (3, 'Kiev');
INSERT INTO locations VALUES
    (4, 'Moskva');
INSERT INTO locations VALUES
    (5, 'New York');
SELECT setval('locations_location_id_seq', 5, true);

--product_size
INSERT INTO product_size VALUES
    (1, 'Medium');
INSERT INTO product_size VALUES
    (2, 'Small');
INSERT INTO product_size VALUES
    (3, 'Large');
INSERT INTO product_size VALUES
    (4, 'XLarge');
INSERT INTO product_size VALUES
    (5, 'XSmall');
SELECT setval('product_size_size_id_seq', 5, true);

--products
INSERT INTO products VALUES
    (1, 'Shoulder Knot Leopard Print Dress',50,1,1,1);
INSERT INTO products VALUES
    (2, 'Buckle Belted Rolled Hem PU Shorts',47.50,2,2,2);
INSERT INTO products VALUES
    (3, 'Ruffle Trim Striped Top And High Split Side Pants Set',85.90,3,3,3);
INSERT INTO products VALUES
    (4, 'Crisscross Open Back Dot Strappy Romper',120.20,4,4,4);
INSERT INTO products VALUES
    (5, 'Paperbag Waist Tie Slim Fit Pants',130.50,5,5,5);
SELECT setval('products_product_id_seq', 5, true);

--stocks
INSERT INTO stocks VALUES
    (1,1,5,1);
INSERT INTO stocks VALUES
    (2,2,14,2);
INSERT INTO stocks VALUES
    (3,3,7,3);
INSERT INTO stocks VALUES
    (4,4,6,4);
INSERT INTO stocks VALUES
    (5,5,12,5);
SELECT setval('stocks_stocks_id_seq', 5, true);