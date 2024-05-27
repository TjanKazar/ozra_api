import py2psql
import psycopg2
import json
import Tekmovanje
import Rezultat
from flask import Flask, jsonify, request
import datetime
import poslogika
from flask_cors import CORS

conn = psycopg2.connect(user=py2psql.username,
                        password=py2psql.pwd,
                        host=py2psql.hostname,
                        port=py2psql.port_id,
                        database=py2psql.database)
cur = conn.cursor()

app = Flask("ozraAPI")
CORS(app)

#NAMIZNA ADMINISTRATORSKA APLIKACIJA
#desktop 1
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

#desktop 2
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

#desktop 3
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

#desktop 4
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
#desktop 5
@app.post("/obvestilo")
def post_obvestilo():
    data = request.get_json()
    title = data["title"]
    body = data["body"]
    query = "INSERT INTO obvestilo (title, body) values (%s, %s)"
    cur.execute(query, (title, body))
    conn.commit()
    return jsonify ({"message": "obvestilo added"})
#desktop 6
@app.post("/dogodek")
def post_dogodek():
    data = request.get_json()
    tekmovanje_ID = data["objava_ID"]
    objava_ID = data["objava_ID"]
    query = "INSERT INTO objava (tekmovanje_ID, objava_ID) VALUES (%s, %s)"
    cur.execute(query, (tekmovanje_ID, objava_ID))
    conn.commit()
    return jsonify({"message": "objava added"})

#desktop 7
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

@app.get('/swimmers/<string:name>')
def get_best_swimmers(name, surname):
    query = """
        SELECT rezultat.*
        FROM rezultat
        JOIN rezultat_tekmovanje ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID
        JOIN swimmer ON swimmer.ID = rezultat.Swimmer_ID
        WHERE swimmer.name = %s AND swimmer.surname = %s
    """
    cur.execute(query, (name, surname))
    rows = cur.fetchall()

    if not rows:
        return jsonify({"error": f"No results found for swimmer with the name {name} {surname}"}), 404

    top_swimmer_ids = poslogika.get_top_swimmers(rows)

    top_swimmers = []
    for swimmer_id in top_swimmer_ids:
        query2 = "SELECT * FROM rezultat WHERE ID = %s"
        cur.execute(query2, (swimmer_id,))
        top_swimmers.append(cur.fetchone())

    return jsonify(top_swimmers)


@app.get('/runners/<string:name>/<string:surname>')
def get_best_runners(name, surname):

    full_name = name.capitalize() + " " + surname.capitalize()
    # First, find the competitors with the given name and surname in the rezultat table
    query = """
    SELECT rezultat_tekmovanje.Rezultat_ID, rezultat.run
    FROM rezultat_tekmovanje
    JOIN rezultat ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID
    WHERE rezultat.name = %s 
    """
    cur.execute(query, (full_name,))
    rows = cur.fetchall()

    # Assume poslogika.get_top_runners is defined to get the top runner IDs from the rows
    top_runner_ids = poslogika.get_shortest_time_run(rows)

    top_runners = []
    for runner_id in top_runner_ids:
        query2 = "SELECT * FROM rezultat WHERE ID = %s"
        cur.execute(query2, (runner_id,))
        top_runners.append(cur.fetchone())

    return jsonify(top_runners)

@app.get('/bikers/<string:name>')
def get_best_bikers(name, surname):
    query = """
        SELECT rezultat.*
        FROM rezultat
        JOIN rezultat_tekmovanje ON rezultat_tekmovanje.Rezultat_ID = rezultat.ID
        JOIN biker ON biker.ID = rezultat.Biker_ID
        WHERE biker.name = %s AND biker.surname = %s
    """
    cur.execute(query, (name, surname))
    rows = cur.fetchall()

    if not rows:
        return jsonify({"error": f"No results found for biker with the name {name} {surname}"}), 404

    top_biker_ids = poslogika.get_top_bikers(rows)

    top_bikers = []
    for biker_id in top_biker_ids:
        query2 = "SELECT * FROM rezultat WHERE ID = %s"
        cur.execute(query2, (biker_id,))
        top_bikers.append(cur.fetchone())

    return jsonify(top_bikers)


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
#desktop 8, web 3, web 4

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
    data = poslogika.get_shortest_time(result)

    return jsonify(data)




    data = poslogika.get_shortest_time_swim(result)

    return jsonify(data)

@app.get('/tekmovalec_run/<name>/<surname>')
def get_porocilo_tekmovalca_tekme_run(name, surname):
    full_name = name.capitalize() + " " + surname.capitalize()
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (full_name,))
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

@app.get('/tekmovalec_bike/<name>/<surname>')
def get_porocilo_tekmovalca_tekme_bike(name, surname):
    full_name = name.capitalize() + " " + surname.capitalize()
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (full_name,))
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

@app.get('/tekmovalec_swim/<name>/<surname>')
def get_porocilo_tekmovalca_tekme_swim(name, surname):
    full_name = name.capitalize() + " " + surname.capitalize()
    query = "SELECT * FROM rezultat WHERE name = %s"
    cur.execute(query, (full_name,))
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
#desktop 9
@app.put('/change_access')
def change_access():
    data = request.get_json()
    value = data["accessible"]
    id = data["id"]
    cur.execute("UPDATE uporabnik SET accessible = %s WHERE id = %s", (value, id))
    conn.commit()
    return jsonify({"message": "User access updated"})



    data = poslogika.get_shortest_time_bike(result)

    return jsonify(data)

#desktop 10, web 2
@app.post('/uporabnik_tekmovanje_post')
def uporabnik_tekmovanje_post():
    data = request.get_json()
    tk_uporabnik = data["uporabnik_id"]
    tk_tekmovanje = data["tekmovanje_id"]
    cur.execute("INSERT INTO uporabnik_tekmovanje (uporabnik_id, tekmovanje_id) VALUES (%s, %s)", (tk_uporabnik, tk_tekmovanje))
    conn.commit()
    return "uporabnik_tekmovanje added"

#SPLETNA UPORABNIŠKA APLIKACIJA
#web 1
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

#web 5
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
#web 6
@app.put("/rating")
def put_objava_rating():
     data = request.get_json()
     id = data["id"]
     upvote = data["upvote"]
     downvote = data["downvote"]
     if (upvote == 1) :
        select_upvote = "SELECT upvote FROM objava WHERE id = %s"
        cur.execute(select_upvote, (id,))
        upvotes_current = cur.fetchone()[0]
        upvotes_new = upvotes_current + 1
        change_rating = "UPDATE objava SET upvote = %s where id = %s"
        cur.execute(change_rating, (upvotes_new, id))
        conn.commit()
     elif (downvote == 1):
        select_downvote = "SELECT downvote FROM objava WHERE id = %s"
        cur.execute(select_downvote, (id,))
        downvotes_current = cur.fetchone()[0]
        downvotes_new = downvotes_current + 1
        change_rating = "UPDATE objava SET downvote = %s where id = %s"
        cur.execute(change_rating, (downvotes_new, id))
        conn.commit()

     return jsonify({"message": "rating updated"})

#web 7

@app.post('/follow')
def post_follow():
     data = request.get_json()
     follower = data["follower"]
     followed = data["followed"]
     query = "INSERT INTO follow (follower, followed) values (%s, %s)"
     cur.execute(query, (follower, followed))
     conn.commit()
     return jsonify({"message": "follow added"})
#web 8
@app.delete('/delete_objava/<int:id>')
def objava_delete(id):
     data = request.get_json()
     objava_id = data["objava_id"]
     autor_id = data["autor_id"]
     get_objava_query = "SELECT autor_id FROM objava WHERE id = %s"
     cur.execute(get_objava_query, (id,))
     result_id = cur.fetchone()  # Fetch the result from the query
     if result_id is not None:
         result_id_int = result_id[0]
         if result_id_int == autor_id:
            query = "DELETE FROM objava WHERE id = %s"
            cur.execute(query, (objava_id,))
            conn.commit()
            return jsonify({"message": "objava deleted"})
         else:
            return jsonify({"message": "error, user cant delete this objava"})
     else:
          return jsonify({"message": "error, objava with given ID not found"})

#web 9
     
@app.get('/uporabnik/<string:name>/<string:password>')
def get_uporabnik(name, password):
    # Query to find the first user with the given name and password
    cur.execute("SELECT * FROM uporabnik WHERE name = %s AND password = %s LIMIT 1", (name, password))
    user = cur.fetchone()

    if user:
        user_data = {
            "id": user[0],
            "name": user[1],
            "surname": user[2],
            "birth_date": user[3],
            "password": user[4],
            "accessible": user[5]
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404
#web 10

@app.get("/obvestila/<int:id>")
def obvestila_get(id):
    query = "SELECT * FROM obvestilo WHERE user_fk = %s"
    cur.execute(query, (id,))
    rows = cur.fetchall()
    result = []
    for row in rows:
         result.append({
              "title": row[1],
              "user_tk": row[2],
              "body": row[3]
         })
    return result

if __name__ == '__main__':
    app.run()
cur.close()
conn.close()
print("PostgreSQL connection is closed")