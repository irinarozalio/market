import unittest
import requests
from market import f1

class TestProduct1(unittest.TestCase):	
	def test_product(self):
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/amount_product?product_id=1"
		r = requests.get(url)
		self.assertEqual(r.json()['name'], 'Shoulder Knot Leopard Print Dress')

class TestProduct2(unittest.TestCase):	
	def test_product(self):
		url = r"http://ec2-3-17-162-33.us-east-2.compute.amazonaws.com:5000/amount_product?product_id='a'"
		r = requests.get(url)
		self.assertEqual(r.json()['error'], 'No Product Found')

	def test_f1(self):
		self.assertGreaterEqual(1, f1())

# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()