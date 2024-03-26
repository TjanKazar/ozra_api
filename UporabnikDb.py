import json
import os
import psycopg2
import time
import py2psql
from datetime import datetime
from Tekmovanje import Tekmovanje
from Rezultat import Rezultat

current_dir = os.path.dirname(os.path.abspath(__file__))

filename = r"uporabniki_JSON.json"

json_file_path = os.path.join(current_dir, filename)

with open(json_file_path, 'r') as file:
    uporabnik_data = json.load(file)

conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()
drop_uporabnik_table = "DROP TABLE IF EXISTS uporabnik;"
cur.execute(drop_uporabnik_table)
conn.commit()
create_uporabnik_table = '''CREATE TABLE uporabnik
    (ID SERIAL PRIMARY KEY  NOT NULL,
    name                    TEXT,
    surname                 TEXT,
    birth_date              TEXT,
    password                TEXT,
    accessible              BOOLEAN); '''
cur.execute(create_uporabnik_table)
conn.commit()

uporabnik_insert_query = """INSERT INTO uporabnik 
    (name, surname, birth_date, password, accessible) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

for key, value in uporabnik_data.items():
    uporabnik_values = (
        value["name"],
        value["surname"],
        value["birth_date"],
        value["password"],
        value["accessible"],
    )
    cur.execute(uporabnik_insert_query, uporabnik_values)
    conn.commit()

zacetek = time.time()
zacetekDatetime = datetime.fromtimestamp(zacetek).strftime('%Y-%m-%d %H:%M:%S')
print("začetek : " + str(zacetekDatetime))

cur.close()
conn.close()