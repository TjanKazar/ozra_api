import py2psql
import psycopg2
import json
from flask import Flask
from flask_restful import Resource, Api

conn = psycopg2.connect(user=py2psql.username,
                        password=py2psql.pwd,
                        host=py2psql.hostname,
                        port=py2psql.port_id,
                        database=py2psql.database)

cur = conn.cursor()


app = Flask("ozraAPI")
api = Api(app)

class Tekmovanje(Resource):

    def get(self):
        return "hello Wrld"
    
api.add_resource(Tekmovanje, '/')

if __name__ == '__main__':
    app.run()

urls = ('/api/rezultat/(.+)','Rezultat')

cur.close()
conn.close()
print("PostgreSQL connection is closed")