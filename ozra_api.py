import py2psql
import psycopg2
import json
import Tekmovanje
import Rezultat
from flask import Flask, jsonify, request
import datetime
import poslogika

# attempt 1

def get_shortest_time(rows):
    min_time = float('inf')
    min_time_entry = None

    for row in rows:
        overall_time_str = row['overall']
        
        try:
            overall_time = datetime.datetime.strptime(overall_time_str, '%H:%M:%S')
        except ValueError:
            continue

        total_seconds = overall_time.hour * 3600 + overall_time.minute * 60 + overall_time.second
        
        if total_seconds < min_time:
            min_time = total_seconds
            min_time_entry = row

    return min_time_entry

conn = psycopg2.connect(user=py2psql.username,
                        password=py2psql.pwd,
                        host=py2psql.hostname,
                        port=py2psql.port_id,
                        database=py2psql.database)
cur = conn.cursor()

app = Flask("ozraAPI")

@app.get("/tekmovanja")
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
        #asdf 
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
    cur.execute(query, (id))
    row = cur.fetchone()
    result = {
        "id": row[0],
        "competition_name": row[1],  
        "year": row[2], 
        "results": row[3], 
            }
    return jsonify(result)

@app.get('/tekmovanje_year/<year>')
def get_tekmovanje_year(year):
    query = "SELECT * FROM Tekmovanje WHERE year = %s"
    cur.execute(query, (year,))
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append ({
            "id": row[0],
            "competition_name": row[1],  
            "year": row[2], 
            "results": row[3], 
                })
    return jsonify(result)

@app.get('/tekmovanje_name/<competition_name>')
def get_tekmovanje_name(competition_name):
    query = "SELECT * FROM Tekmovanje WHERE competition_name = %s"
    cur.execute(query, (competition_name,))
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append ({
            "id": row[0],
            "competition_name": row[1],  
            "year": row[2], 
            "results": row[3], 
                })
    return jsonify(result)

@app.get('/porocilotekmovanja/<int:id>')
def get_porocilo(id):
    query = "SELECT Rezultat_ID FROM rezultat_tekmovanje WHERE Tekmovanje_ID = %s"
    cur.execute(query, (id,))
    rows = cur.fetchall()

    nastopi = []
    for row in rows:
        rezultat_id = row[0]
        query2 = "SELECT * FROM rezultat WHERE id = %s"
        cur.execute(query2, (rezultat_id,))
        nastopi.append(cur.fetchone())

    cas_plavanja = []
    cas_plavanja.append(nastopi)
    return jsonify(nastopi)

@app.get('/swimmers/<int:id>')
def get_bestSwimmers(id):
    query = "SELECT Rezultat_ID, swim FROM rezultat_tekmovanje JOIN rezultat ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID WHERE Tekmovanje_ID = %s"
    cur.execute(query, (id,))
    rows = cur.fetchall()

    swim_times = {}
    for row in rows:
        rezultat_id = row[0]
        swim_time = row[1]
        if swim_time != '---':
            swim_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(swim_time.split(':'))))
            swim_times[rezultat_id] = swim_seconds
    
    shortest_swim_times = sorted(swim_times.items(), key=lambda item: item[1])[:3]
    
    top_3_swimmers = []
    for swimmer_id, _ in shortest_swim_times:
        query2 = "SELECT * FROM rezultat WHERE id = %s"
        cur.execute(query2, (swimmer_id,))
        top_3_swimmers.append(cur.fetchone())

    return jsonify(top_3_swimmers)

@app.get('/runners/<int:id>')
def get_bestRunners(id):
    query = "SELECT Rezultat_ID, run FROM rezultat_tekmovanje JOIN rezultat ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID WHERE Tekmovanje_ID = %s"
    cur.execute(query, (id,))
    rows = cur.fetchall()

    run_times = {}
    for row in rows:
        rezultat_id = row[0]
        run_time = row[1]
        if run_time != '---':
            swim_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(run_time.split(':'))))
            run_times[rezultat_id] = swim_seconds
    
    shortest_run_times = sorted(run_times.items(), key=lambda item: item[1])[:3]
    
    top_3_runners = []
    for runner_id, _ in shortest_run_times:
        query2 = "SELECT * FROM rezultat WHERE id = %s"
        cur.execute(query2, (runner_id,))
        top_3_runners.append(cur.fetchone())

    return jsonify(top_3_runners)

    
@app.get('/bikers/<int:id>')
def get_bestBikers(id):
    query = "SELECT Rezultat_ID, bike FROM rezultat_tekmovanje JOIN rezultat ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID WHERE Tekmovanje_ID = %s"
    cur.execute(query, (id,))
    rows = cur.fetchall()

    bike_times = {}
    for row in rows:
        rezultat_id = row[0]
        bike_time = row[1]
        if bike_time != '---':
            swim_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(bike_time.split(':'))))
            bike_times[rezultat_id] = swim_seconds
    
    shortest_bike_times = sorted(bike_times.items(), key=lambda item: item[1])[:3]
    
    top_3_bikers = []
    for biker_id, _ in shortest_bike_times:
        query2 = "SELECT * FROM rezultat WHERE id = %s"
        cur.execute(query2, (biker_id,))
        top_3_bikers.append(cur.fetchone())

    return jsonify(top_3_bikers)



@app.get('/tekmovanje/<competition_name>/<year>')
def get_tekmovanje_name_year(competition_name, year):
    query = "SELECT * FROM Tekmovanje WHERE competition_name = %s AND year = %s"
    cur.execute(query, (competition_name, year))
    row = cur.fetchone()
    result = {
        "id": row[0],
        "competition_name": row[1],  
        "year": row[2], 
        "results": row[3], 
            }
    return jsonify(result)

@app.get('/tekmovalec/<name>')
def get_porocilo_tekmovalca(name):
    name_parsed = poslogika.convert_to_proper_case(name)
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (name_parsed,))
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
    return jsonify(result)


@app.get('/tekmovalec_best_overall/<name>')
def get_porocilo_tekmovalca_best_time(name):
    name_parsed = poslogika.convert_to_proper_case(name)
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (name_parsed,))
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
    data = get_shortest_time(result)

    return jsonify(data)


@app.get('/tekmovalec_swim/<name>')
def get_porocilo_tekmovalca_tekme_swim(name):
    name_parsed = poslogika.convert_to_proper_case(name)
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (name_parsed,))
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

    data = poslogika.get_shortest_time_swim(result)

    return jsonify(data)

@app.get('/tekmovalec_run/<name>')
def get_porocilo_tekmovalca_tekme_run(name):
    name_parsed = poslogika.convert_to_proper_case(name)
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (name_parsed,))
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

    data = poslogika.get_shortest_time_run(result)

    return jsonify(data)
@app.get('/tekmovalec_bike/<name>')
def get_porocilo_tekmovalca_tekme_bike(name):
    name_parsed = poslogika.convert_to_proper_case(name)
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (name_parsed,))
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

    data = poslogika.get_shortest_time_bike(result)

    return jsonify(data)


@app.put('/change_access')
def change_access():
    data = request.get_json()
    value = data["accessible"]
    id = data["id"]
    cur.execute("UPDATE uporabnik SET accessible = %s WHERE id = %s", (value, id))
    conn.commit()
    return jsonify({"message": "User access updated"})




# 10. korak je post za Uporabnik_tekmovanje
@app.post('/uporabnik_tekmovanje_post')
def uporabnik_tekmovanje_post():
    data = request.get_json()
    tk_uporabnik = data["uporabnik_id"]
    tk_tekmovanje = data["tekmovanje_id"]
    cur.execute("INSERT INTO uporabnik_tekmovanje (uporabnik_id, tekmovanje_id) VALUES (%s, %s)", (tk_uporabnik, tk_tekmovanje))
    conn.commit()
    return "uporabnik_tekmovanje added"

#uporabniški app
# 1. korak je get objava, mogoče več getov
@app.get('/Objave')
def objave_get():
    query = "SELECT * FROM objava"
    cur.execute(query)
    result = []
    rows = cur.fetchall()
    for row in rows:
        result.append ({
            "id": row[0],
            "name": row[1],  
            "surname": row[2], 
            "birth_date": row[3],
            "password": row[4],
            "accessible": row[5] 
                })
    return jsonify(result)


@app.get('/Objava/<int:id>')
def objave_get_one(id):
    query = "SELECT * FROM objava where id = %s"
    cur.execute(query, (id,))
    row = cur.fetchone() 
    result = {} 
    if row:
        result = {
            "id": row[0],
            "name": row[1],  
            "surname": row[2], 
            "birth_date": row[3],
            "password": row[4],
            "accessible": row[5] 
        }
    return jsonify(result)

# 3. korak je 8. korak admin appa z le eno možnostjo za id
# 5. korak je post objava, author je user
# 6. korak je put na objava (upvote, downvote)
# 7. korak je folowing, ... /TODO se kak to resit
# 8. korak je delete objava where autor = uporabnik ... /TODO
# 9. korak je put uporabnik
#10. korak je get obvestilo ? /TODO mby naredi class obvestilo



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

@app.post('/objavapost')
def post_objava():
      data = request.get_json()
      title = data.get('title')
      body = data.get('body')
      autor = data.get('autor')
      upvote = data.get('upvote')
      downvote = data.get('downvote')

      cur.execute("""INSERT INTO objava (title, body, autor, upvote, downvote)
                  VALUES (%s, %s, %s, %s, %s)""", (title, body, autor, upvote, downvote))
      conn.commit()
      return jsonify({"message": "Objava posted successfully"}), 201

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