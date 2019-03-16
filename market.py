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
		print(flask.request.args.get('ohad'))
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		pg_cur.execute("select product_id, name from products")
		res = [dict(record) for record in pg_cur]
		return res

class Locations(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		pg_cur.execute("select * from locations")
		res = [dict(record) for record in pg_cur]
		return res

class Amount(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		print(flask.request.args.get('product_id'))
		try:
			pg_cur.execute("""SELECT p.name, s.amount 
							FROM products p 
							INNER JOIN stocks s 
							ON p.product_id = s.product_id 
							where p.product_id=%(product_id)s""", 
							{'product_id': flask.request.args.get('product_id')})
			# res = [dict(record) for record in pg_cur]
			return dict(pg_cur.fetchone())
		except TypeError as err:
			print("NoneType: {0}".format(err) + "Validation is failed")				
		except Exception as err:
			print(err)
			print_tb(traceback.print_tb(err.__traceback__))


def config(filename='database.ini', section='postgresql'):
	# create a parser
	parser = ConfigParser()
	# read config file
	parser.read(filename)
 
	# get section, default to postgresql
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, filename))
	return db
 
def connect():
	""" Connect to the PostgreSQL database server """
	conn = None
	try:
		# read connection parameters
		params = config()
		print (params)
		# connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)
		conn.autocommit = True
		# create a cursor
		cur = conn.cursor()       
		# execute a statement
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')

		# display the PostgreSQL database server version
		db_version = cur.fetchone()
		print(db_version)
		# close the communication with the PostgreSQL
		#cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	# finally:
	# 	if conn is not None:
	# 		conn.close()
	# 		print('Database connection closed.')
	return conn

pg_con = connect()
# pg_con.autocommit = True

api.add_resource(CTest, '/test')
api.add_resource(Locations, '/locations')
api.add_resource(All_Products, '/all_products')
api.add_resource(Amount, '/amount_product')


if __name__ == '__main__':
	connect()
	app.run(debug=True, host='0.0.0.0')