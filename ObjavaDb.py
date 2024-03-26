import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime


json_string_location = r"C:\Users\tjank\OneDrive - Univerza v Mariboru\git_repos\Orodja-za-razvoj-aplikacij\objave_JSON.json"
with open(json_string_location, 'r') as file:
    objava_data = json.load(file)

conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()
drop_objava_table = "DROP TABLE IF EXISTS objava;"
cur.execute(drop_objava_table)
conn.commit()

create_objava_table = '''CREATE TABLE objava
    (ID SERIAL PRIMARY KEY  NOT NULL,
    title                   TEXT,
    body                TEXT,
    autor                   TEXT,
    upvote                  INTEGER,
    downvote                INTEGER,
    visible                 BOOLEAN); '''
cur.execute(create_objava_table)
conn.commit()

objava_insert_query = """INSERT INTO objava 
    (title, body, autor, upvote, downvote, visible) 
    VALUES (%s, %s, %s, %s, %s, %s)"""

for key, value in objava_data.items():
    objava_values = (
        value["title"],
        value["body"],
        value["autor"],
        value["upvote"],
        value["downvote"],
        value["visible"]
    )
    cur.execute(objava_insert_query, objava_values)
    conn.commit()

zacetek = time.time()
zacetekDatetime = datetime.fromtimestamp(zacetek).strftime('%Y-%m-%d %H:%M:%S')
print("začetek : " + str(zacetekDatetime))

cur.close()
conn.close()
