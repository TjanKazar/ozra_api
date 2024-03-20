import py2psql
import Rezultat
import Tekmovanje
import psycopg2
import json
from flask import Flask, jsonify, request
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
            cur.execute("SELECT * FROM Tekmovanje")
            rows = cur.fetchall()
            result = []
            for row in rows:
                result.append({
                    "id": row[0],
                    "competition_name": row[1],  
                    "year": row[2], 
                     "results": row[3], 
                })
            return jsonify(result)

t = Tekmovanje

class Tekmovanje(Resource):
    def get(self):
            cur.execute("SELECT * FROM Tekmovanje")
            rows = cur.fetchall()
            result = []
            for row in rows:
                result.append({
                    "id": row[0],
                    "competition_name": row[1],  
                    "year": row[2], 
                     "results": row[3], 
                })
            return jsonify(result)


class Rezultat(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10)) 
            
        cur.execute("SELECT COUNT(*) FROM Rezultat")
        total_rows = cur.fetchone()[0]
            
        total_pages = (total_rows + limit - 1) // limit 
            
        offset = (page - 1) * limit
            
        query = "SELECT * FROM Rezultat LIMIT %s OFFSET %s"
        cur.execute(query, (limit, offset))
            
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "swim": row[1],
                "division": row[2],
                "run": row[3],
                "name": row[4],
                "profession": row[5],
                "country": row[6],
                "age": row[7],
                "run_distance": row[8],
                "bib": row[9],
                "state": row[10],
                "bike": row[11],
                "gender_rank": row[12],
                "overall": row[13],
                "swim_distance": row[14],
                "overall_rank": row[15],
                "points": row[16],
                "t2": row[17],
                "bike_distance": row[18],
                "t1": row[19],
                "div_rank": row[20]
            })
        return jsonify({
            "total_rows": total_rows,
            "total_pages": total_pages,
            "current_page": page,
            "data": result
        })
t = Tekmovanje
r = Rezultat

api.add_resource(t, '/Tekmovanja')
api.add_resource(r, '/Rezultati')

if __name__ == '__main__':
    app.run()

urls = ('/api/rezultat/(.+)','Rezultat')

cur.close()
conn.close()
print("PostgreSQL connection is closed")