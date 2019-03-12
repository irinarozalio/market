from flask import Flask, jsonify
from flask_restful import Resource, Api
import psycopg2
import psycopg2.extras
import json
import flask

app = Flask(__name__)
api = Api(app)

class CTest(Resource):
	def get(self):
		pg_cur = pg_con.cursor()
		pg_cur.execute("select to_char(now(), 'DD/MM/YYYY HH24:MI:SS') as date_")
		date_now = pg_cur.fetchone()[0]
		return {'Dates': date_now + '123'}

class Locations(Resource):
	def get(self):
		pg_cur = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		pg_cur.execute("select * from locations")
		res = [dict(record) for record in pg_cur]
		return res

pg_con = psycopg2.connect(database='dev',
						user='iradba',
						password='Unix11',
						host = 'ip-172-31-12-93',
						port = '5432')
pg_con.autocommit = True

api.add_resource(CTest, '/test')
api.add_resource(Locations, '/locations')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')