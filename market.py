from flask import Flask, jsonify
from flask_restful import Resource, Api
import psycopg2
import psycopg2.extras
import json
import flask
from configparser import ConfigParser
#from config import config
import config
import traceback
import os
from dotenv import load_dotenv


load_dotenv('.env')

app = Flask(__name__)
api = Api(app)

class CTest(Resource):
	# def get(self):
		# pg_cur = pg_con.cursor()
		# pg_cur.execute("select to_char(now(), 'DD/MM/YYYY HH24:MI:SS') as date_")
		# date_now = pg_cur.fetchone()[0]
		# return {'Dates': date_now + '123'}

	def put(self):
		print (flask.request.form['data'])
		return {'123':'123'}


class All_Products(Resource):
	def get(self):
		print(flask.request.args.get('ira'))
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		pg_cur.execute("select product_id, name from products")
		res = [dict(record) for record in pg_cur]
		return res

class Locations(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		pg_cur.execute("select location_id, location_name from locations")
		res = [dict(record) for record in pg_cur]
		return res

	def put(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		# print (flask.request.form['location_name'])
		pg_cur.execute('''INSERT INTO locations (location_name) 
						  VALUES (%(location_name)s)
						  RETURNING location_id ''',
						  {'location_name': flask.request.form['location_name']})

		return {'location_id': pg_cur.fetchone()['location_id']}

class Check_Locations(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print(flask.request.args.get('location_id'))
		pg_cur.execute("""SELECT location_id, location_name
						FROM locations 
						where location_id=%(location_id)s""", 
						{'location_id': flask.request.args.get('location_id', 0, int)})
		row = pg_cur.fetchone()
		return dict(row) if row else {'error': 'No Product Found'}

class Amount(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print(flask.request.args.get('product_id'))
		#try:
		pg_cur.execute("""SELECT p.name, s.amount 
						FROM products p 
						INNER JOIN stocks s 
						ON p.product_id = s.product_id 
						where p.product_id=%(product_id)s""", 
						{'product_id': flask.request.args.get('product_id', 0, int)})
		# res = [dict(record) for record in pg_cur]
		row = pg_cur.fetchone()
		return dict(row) if row else {'error': 'No Product Found'}

class Reduce_Amount(Resource):
	def put(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print (flask.request.form['amount'])
		pg_cur.execute('''SELECT product_id, amount from stocks 
						where product_id=%(product_id)s
						and location_id=%(location_id)s''',
						{'product_id': flask.request.form['product_id'],
						'location_id': flask.request.form['location_id']})
		row = pg_cur.fetchone()
		if row is None:
			return [{'amount': flask.request.form['amount']},
			        {flask.request['product_id']: 'Sold out'}]
		else:
			row = dict(row)
			stock_amount = row['amount'] 
			if stock_amount == 0:
				return{row['product_id']: 'Not in stock'}
			else:
				remain = stock_amount - int(flask.request.form['amount'])
				if remain > 0:
					pg_cur.execute('''UPDATE stocks
						set amount=%(remain)s
						where product_id=%(product_id)s 
						and location_id=%(location_id)s
						RETURNING amount, product_id''',
						{'remain': remain,
						'product_id': flask.request.form['product_id'],
						'location_id': flask.request.form['location_id']})
					return [{row['product_id']: 'Normal Sale'},
							{'Remain': remain}]
				else:
					pg_cur.execute('''UPDATE stocks
					set amount=0
					where product_id=%(product_id)s 
					and location_id=%(location_id)s
					RETURNING amount, product_id''',
					{'product_id': flask.request.form['product_id'],
					'location_id': flask.request.form['location_id']})
					if remain==0:
						return [{row['product_id']: 'Sold out'}]
					else:
						return [{row['product_id']: 'Sold out'},
								{'Overamount': int(flask.request.form['amount']) - stock_amount}]
					
		# pg_cur.execute('''UPDATE stocks
		# 				set amount= amount - %(amount)s
		# 				where product_id=%(product_id)s 
		# 				and location_id=%(location_id)s
		# 				and (amount - %(amount)s) >= 0
		# 				RETURNING amount, product_id''',
		# 				{'amount': flask.request.form['amount'] ,
		# 				'product_id': flask.request.form['product_id'] ,
		# 				'location_id': flask.request.form['location_id']})
		# a = pg_cur.fetchone()		
		# if a is not None:
		# 	a = dict(a)
		# 	if a['amount'] == 0:
		# 		return{a['product_id']: 'Sold out'}
		# 	else:
		# 		return {'amount': a['amount'],
		# 			'product_id': a['product_id']
		# 			}
		# else:
		# 	return{flask.request.form['product_id']: 'Try to Sold overamount'}

			#return{flask.request['product_id']: 'Sold out'}
		# if a is not None:
		# 	a = dict(pg_cur.fetchone())
		# 	return {'amount': a['amount'],
		# 		'product_id': a['product_id']
		# 		}
		# else:
		# 	print('IRA')
		# 	return{flask.request['product_id']: 'Sold out'}
		# return {'amount': a['amount'],
		# 		'product_id': a['product_id']
		# 		}

class Add_Amount(Resource):
	def put(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print (flask.request.form['amount'])
		print(pg_cur)
		pg_cur.execute('''UPDATE stocks
						set amount= amount + %(amount)s
						where product_id=%(product_id)s 
						and location_id=%(location_id)s
						RETURNING amount, product_id''',
						{'amount': flask.request.form['amount'] ,
						'product_id': flask.request.form['product_id'] ,
						'location_id': flask.request.form['location_id']})
		a = pg_cur.fetchone()
		return {'amount': a['amount'],
				'product_id': a['product_id']
				}

class Set_Amount(Resource):
	def put(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print (flask.request.form['amount'])
		print(pg_cur)
		pg_cur.execute('''UPDATE stocks
						set amount=%(amount)s
						where product_id=%(product_id)s 
						and location_id=%(location_id)s
						RETURNING amount, product_id''',
						{'amount': flask.request.form['amount'] ,
						'product_id': flask.request.form['product_id'] ,
						'location_id': flask.request.form['location_id']})
		a = pg_cur.fetchone()
		return {'amount': a['amount'],
				'product_id': a['product_id']
				}

pg_con = psycopg2.connect(database='dev',
						user='iradba',
						password=os.getenv('MARKET_DB_PASS'),
						host = 'ip-172-31-12-93',
						port = '5432')
pg_con.autocommit = True

api.add_resource(CTest, '/test')
api.add_resource(Locations, '/locations')
api.add_resource(All_Products, '/all_products')
api.add_resource(Amount, '/amount_product')
api.add_resource(Check_Locations, '/check_locations')
api.add_resource(Reduce_Amount, '/reduce_amount')
api.add_resource(Add_Amount, '/add_amount')
api.add_resource(Set_Amount, '/set_amount')

def f1():
	return 1

if __name__ == '__main__':
	#connect()
	app.run(debug=True, host='0.0.0.0')