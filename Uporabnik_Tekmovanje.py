import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))

filename = r"objava_tekmovanje_JSON.json"

json_file_path = os.path.join(current_dir, filename)


with open(json_file_path, 'r') as file:
    objava_data = json.load(file)

conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()

drop_objava_table = "DROP TABLE IF EXISTS uporabnik_tekmovanje;"
cur.execute(drop_objava_table)
conn.commit()

create_uporabnik_tekmovanje_table = '''CREATE TABLE uporabnik_tekmovanje (
    ID SERIAL PRIMARY KEY NOT NULL,
    Uporabnik_ID INTEGER REFERENCES Uporabnik(ID),
    Tekmovanje_ID INTEGER REFERENCES Tekmovanje(ID),
    UNIQUE (Uporabnik_ID, Tekmovanje_ID)
);'''
cur.execute(create_uporabnik_tekmovanje_table)
conn.commit()

uporabnik_tekmovanje_insert_query = """INSERT INTO uporabnik_tekmovanje 
    (Uporabnik_ID, Tekmovanje_ID) 
    VALUES (%s, %s)"""

for key, value in objava_data.items():
    uporabnik_tekmovanje_values = (
        value["Uporabnik_ID"],
        value["Tekmovanje_ID"]
    )
    cur.execute(uporabnik_tekmovanje_insert_query, uporabnik_tekmovanje_values)
    conn.commit()

zacetek = time.time()
zacetekDatetime = datetime.fromtimestamp(zacetek).strftime('%Y-%m-%d %H:%M:%S')
print("začetek : " + str(zacetekDatetime))

cur.close()
conn.close()
