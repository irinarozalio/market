import unittest
import requests
from market import f1
import psycopg2
import psycopg2.extras
import os

class Product_name_exist(unittest.TestCase):	
	def test_product_exists(self):
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/amount_product?product_id=1"
		r = requests.get(url)
		self.assertEqual(r.json()['name'], 'Shoulder Knot Leopard Print Dress')

class Product_name_not_exists(unittest.TestCase):	
	def test_product_not_exists(self):
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/amount_product?product_id='a'"
		r = requests.get(url)
		self.assertEqual(r.json()['error'], 'No Product Found')

	# def test_f1(self):
	# 	self.assertGreaterEqual(1, f1())

class Not_in_stock(unittest.TestCase):	
	def test_not_in_stock(self):
		product_id = 1
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/reduce_amount"
		r = requests.put(url, data = {'amount':1, 'product_id':product_id, 'location_id':1 })
		data = r.json()
		#if str(product_id) in data.keys():
		if 'Not in stock' in data.values():
			val = data[str(product_id)]
		else:
			val ='123'
		self.assertEqual(str(val), 'Not in stock')

class ConnectPG(unittest.TestCase):
	pg_con = None
	def test_connectPG(self):
		pg_con = psycopg2.connect(database='dev',
						user='iradba',
						password=os.getenv('MARKET_DB_PASS'),
						host = 'ip-172-31-12-93',
						port = '5432')
		pg_con.autocommit = True
		pg_cur = pg_con.cursor()       
		pg_cur.execute('SELECT version()')
		db_version = pg_cur.fetchone()
		a = 'PostgreSQL 11.2 (Debian 11.2-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit'
		if a in db_version:
			val = 'PostgreSQL 11.2'
		else:
			val ='Database connection closed'
			print('Database connection closed')
		self.assertEqual(val,'PostgreSQL 11.2')

class Set_amount(unittest.TestCase):	
	def test_set_amount(self):
		product_id = 1
		amount = 5
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/set_amount"
		r = requests.put(url, data = {'amount':amount, 'product_id':product_id, 'location_id':1 })
		data = r.json()
		if amount in data.values():
			val = amount
		else:
			print('Test_set_amount is Failed')
		self.assertEqual(val, 5)
	


# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()