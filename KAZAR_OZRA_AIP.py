import py2psql
import psycopg2
import json
import Tekmovanje
from flask import Flask, jsonify, request

conn = psycopg2.connect(user=py2psql.username,
                        password=py2psql.pwd,
                        host=py2psql.hostname,
                        port=py2psql.port_id,
                        database=py2psql.database)
cur = conn.cursor()

app = Flask("ozraAPI")

@app.get("/asdf")
def get_tekmovanja():
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

@app.get('/rezultati')
def get_rezultati():
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

@app.get("/rezultat/<int:id>")
def get_rezultat(id):
    query = "SELECT * FROM Rezultat WHERE id = %s"
    cur.execute(query, (id,))
    row = cur.fetchone()

    result = {
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
        }
    return jsonify(result)

@app.get('/tekmovanje/<int:id>')
def get_tekmovanje(id):
    query = "SELECT * FROM Tekmovanje WHERE id = %s"
    cur.execute(query, (id,))
    row = cur.fetchone()
    result = {
        "id": row[0],
        "competition_name": row[1],  
        "year": row[2], 
        "results": row[3], 
            }
    return jsonify(result)

@app.post("/rezultatpost")
def post_rezultat():
        data = request.get_json()

        swim = data.get('swim')
        division = data.get('division')
        run = data.get('run')
        name = data.get('name')
        profession = data.get('profession')
        country = data.get('country')
        age = data.get('age')
        run_distance = data.get('run_distance')
        bib = data.get('bib')
        state = data.get('state')
        bike = data.get('bike')
        gender_rank = data.get('gender_rank')
        overall = data.get('overall')
        swim_distance = data.get('swim_distance')
        overall_rank = data.get('overall_rank')
        points = data.get('points')
        t2 = data.get('t2')
        bike_distance = data.get('bike_distance')
        t1 = data.get('t1')
        div_rank = data.get('div_rank')

        cur.execute("""
            INSERT INTO Rezultat (swim, division, run, name, profession, country, age, run_distance,
                                    bib, state, bike, gender_rank, overall, swim_distance, overall_rank,
                                    points, t2, bike_distance, t1, div_rank)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (swim, division, run, name, profession, country, age, run_distance, bib, state, bike,
                gender_rank, overall, swim_distance, overall_rank, points, t2, bike_distance, t1, div_rank))

        conn.commit()

        return jsonify({"message": "Result added successfully"}), 201  

@app.post('/Tekmovanjepost')
def post_tekmovanje():
        data = request.get_json()
        competition_name = data.get('competition_name')
        year = data.get('year')
        results = data.get('results')

        cur.execute("""
            INSERT INTO tekmovanje (competition_name, year, results)
            VALUES (%s, %s, %s)""", (competition_name, year, results))
        
        conn.commit()

        return jsonify({"message": "Result added successfully"}), 201  

@app.delete('/tekmovanjedelete')
def delete_tekmovanje():
        data = request.get_json()
        id = data.get('id')
        cur.execute("DELETE FROM tekmovanje WHERE id = %s", (id,))
        
        conn.commit()

        return jsonify({"message": "Result deleted successfully"}), 204  
  
@app.delete('/rezultatdelete')
def delete_rezultat():
        data = request.get_json()
        id = data.get('id')
        cur.execute("DELETE FROM rezultat WHERE id = %s", (id,))
        
        conn.commit()

        return jsonify({"message": "Result deleted successfully"}), 204  

@app.put('/Tekmovanjeput')
def put_tekmovanje():
        data = request.get_json()
        id = data.get('id')
        competition_name = data.get('competition_name')
        year = data.get('year')
        results = data.get('results')

        cur.execute("UPDATE tekmovanje SET competition_name = %s, year = %s, results = %s WHERE id = %s", (competition_name, year, results, id ))
        conn.commit()
        return jsonify({"message": "Result changed successfully"}), 200

@app.put('/Rezultatput')
def put_rezultat():
        data = request.get_json()
        id = data.get('id')
        swim = data.get('swim')
        division = data.get('division')
        run = data.get('run')
        name = data.get('name')
        profession = data.get('profession')
        country = data.get('country')
        age = data.get('age')
        run_distance = data.get('run_distance')
        bib = data.get('bib')
        state = data.get('state')
        bike = data.get('bike')
        gender_rank = data.get('gender_rank')
        overall = data.get('overall')
        swim_distance = data.get('swim_distance')
        overall_rank = data.get('overall_rank')
        points = data.get('points')
        t2 = data.get('t2')
        bike_distance = data.get('bike_distance')
        t1 = data.get('t1')
        div_rank = data.get('div_rank')

        cur.execute("UPDATE rezultat SET swim = %s, division = %s, run = %s, name = %s, profession = %s, country = %s, age = %s, run_distance = %s, bib = %s, state = %s, bike = %s, gender_rank = %s, overall = %s, swim_distance = %s, overall_rank = %s, points = %s, t2 = %s, bike_distance = %s, t1 = %s, div_rank = %s WHERE id = %s", (swim, division, run, name, profession, country, age, run_distance, bib, state, bike, gender_rank, overall, swim_distance, overall_rank, points, t2, bike_distance, t1, div_rank, id))

        conn.commit()
        return jsonify({"message": "Result changed successfully"}), 200

if __name__ == '__main__':
    app.run()
cur.close()
conn.close()
print("PostgreSQL connection is closed")