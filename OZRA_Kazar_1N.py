import json
import os
import psycopg2
import time
import py2psql
from datetime import datetime
from Tekmovanje import Tekmovanje
from Rezultat import Rezultat

def get_rezultat_list(json_paths):
    rezultat_list = []

    for json_path in json_paths:
        with open(json_path, 'r') as json_file:
            json_content = json.load(json_file)
            rezultat_list.extend([Rezultat(**result) for result in json_content.values()])
    return rezultat_list

def get_tekmovanje(json_paths):
    tekmovanja_list = []

    for json_path in json_paths:
        base_name = os.path.basename(json_path)
        parts = os.path.splitext(base_name)[0].split('_')

        competition_name = ' '.join(parts[1:-1]) 
        year = parts[-1]

        rezultati = get_rezultat_list([json_path])

        tekme = Tekmovanje(competition_name=competition_name, year=year, results=len(rezultati))
        tekmovanja_list.append(tekme)

    return tekmovanja_list

def if_missing(data):
    if data == "---":
        return "EMPTY"
    elif len(data) == 0:
        return "EMPTY"
    else:
        return data

script_dir = os.path.dirname(__file__)

race_results_folder = os.path.join(script_dir, "Race-Results")
json_folder_path = os.path.join(race_results_folder, "IRONMAN", "JSON")
json_folder_path_703 = os.path.join(race_results_folder, "IRONMAN70.3", "JSON")

datoteke_im = os.listdir(json_folder_path)
datoteke_json_im = [os.path.join(json_folder_path, f) for f in datoteke_im if f.endswith('.json')]

datoteke_im703 = os.listdir(json_folder_path_703)
datoteke_json_im703 = [os.path.join(json_folder_path_703, f) for f in datoteke_im703 if f.endswith('.json')]

rezultati_im = get_rezultat_list(datoteke_json_im)
rezultati_im703 = get_rezultat_list(datoteke_json_im703)

tekme_im = get_tekmovanje(datoteke_json_im)
tekme_im703 = get_tekmovanje(datoteke_json_im703)

conn = psycopg2.connect(
    host = py2psql.hostname,
    dbname = py2psql.database,
    user = py2psql.username,
    password = py2psql.pwd,
    port = py2psql.port_id)
cur = conn.cursor()

# sql query

zacetek = time.time()
zacetekDatetime = datetime.fromtimestamp(zacetek).strftime('%Y-%m-%d %H:%M:%S')

print("začetek : " + str(zacetekDatetime))

sql = '''DROP table IF EXISTS rezultat '''
cur.execute(sql) 
sql = '''DROP table IF EXISTS tekmovanje'''
cur.execute(sql) 


create_rezultat_table = '''CREATE TABLE rezultat
    (ID SERIAL PRIMARY KEY  NOT NULL,
    swim                    TEXT,
    division                TEXT,
    run                     TEXT,
    name                    TEXT,
    profession              TEXT,
    country                 TEXT,
    age                     TEXT,
    run_distance            TEXT,
    bib                     TEXT,
    state                   TEXT,
    bike                    TEXT,
    gender_rank             TEXT,
    overall                 TEXT,
    swim_distance           TEXT,
    overall_rank            TEXT,
    points                  TEXT,
    t2                      TEXT,
    bike_distance           TEXT,
    t1                      TEXT,
    div_rank                TEXT); '''

cur.execute(create_rezultat_table)
conn.commit()

create_tekmovanje_table =  '''CREATE TABLE tekmovanje    
    (ID SERIAL PRIMARY KEY  NOT NULL,
    competition_name        TEXT,
    year                    TEXT,
    results                 TEXT); '''

cur.execute(create_tekmovanje_table)
conn.commit()

postres_insert_query_rez = """INSERT INTO rezultat 
    (swim, division, run, name, profession, country, age, run_distance, bib, state, bike, gender_rank, overall,swim_distance, overall_rank, points, t2, bike_distance, t1, div_rank) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

for i in range (len(rezultati_im)):
        vpis = (rezultati_im[i].swim,
               rezultati_im[i].division,
               rezultati_im[i].run,
               rezultati_im[i].name,
               rezultati_im[i].profession,
               rezultati_im[i].country,
               rezultati_im[i].age,
               rezultati_im[i].runDistance,
               rezultati_im[i].bib,
               rezultati_im[i].state,
               rezultati_im[i].bike,
               rezultati_im[i].genderRank,
               rezultati_im[i].overall,
               rezultati_im[i].swimDistance,
               rezultati_im[i].overallRank,
               rezultati_im[i].points,
               rezultati_im[i].t2,
               rezultati_im[i].bikeDistance,
               rezultati_im[i].t1,
               rezultati_im[i].divRank)
        cur.execute(postres_insert_query_rez, vpis)
        conn.commit()

for i in range (len(rezultati_im703)):
        vpis1 = (rezultati_im[i].swim,
               rezultati_im[i].division,
               rezultati_im[i].run,
               rezultati_im[i].name,
               rezultati_im[i].profession,
               rezultati_im[i].country,
               rezultati_im[i].age,
               rezultati_im[i].runDistance,
               rezultati_im[i].bib,
               rezultati_im[i].state,
               rezultati_im[i].bike,
               rezultati_im[i].genderRank,
               rezultati_im[i].overall,
               rezultati_im[i].swimDistance,
               rezultati_im[i].overallRank,
               rezultati_im[i].points,
               rezultati_im[i].t2,
               rezultati_im[i].bikeDistance,
               rezultati_im[i].t1,
               rezultati_im[i].divRank)

        cur.execute(postres_insert_query_rez, vpis1)
        conn.commit()

postres_insert_query_tekme = """INSERT INTO tekmovanje 
    (competition_name, year, results) 
    VALUES (%s, %s, %s)"""

for i in range (len(tekme_im)):
    vpis2 = (tekme_im[i].competition_name,
      tekme_im[i].year,
      tekme_im[i].results)
    cur.execute(postres_insert_query_tekme, vpis2)
    conn.commit()


for i in range (len(tekme_im703)):
    vpis3 = (tekme_im703[i].competition_name,
      tekme_im703[i].year,
      tekme_im703[i].results)
    cur.execute(postres_insert_query_tekme, vpis3)
    conn.commit()

konec = time.time()
trajanje = konec - zacetek
konecDatetime = datetime.fromtimestamp(konec).strftime('%Y-%m-%d %H:%M:%S')

print("konec : " + str(konecDatetime))
print("skupni čas v sekundah : "+ str(trajanje))
cur.close()
conn.close()