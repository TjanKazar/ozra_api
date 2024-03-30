import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = r"obvestila_JSON.json"
json_file_path = os.path.join(current_dir, filename)

with open(json_file_path, 'r') as file:
    obvestilo_data = json.load(file)

conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()

drop_obvestilo_table = "DROP TABLE IF EXISTS obvestilo;"
cur.execute(drop_obvestilo_table)
conn.commit()

create_obvestilo_table = '''CREATE TABLE obvestilo (
    ID SERIAL PRIMARY KEY NOT NULL,
    title   TEXT,
    user_fk INTEGER,
    body    TEXT
);'''
cur.execute(create_obvestilo_table)

obvestilo_insert_query = """INSERT INTO obvestilo
    (title, user_fk, body)
    VALUES (%s, %s, %s)"""

for item in obvestilo_data:
    obvestilo_values = (
        item["title"],
        item["user_fk"],
        item["body"]
    )
    cur.execute(obvestilo_insert_query, obvestilo_values)

conn.commit()

cur.close()
conn.close()
