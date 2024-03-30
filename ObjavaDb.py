import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))

filename = r"objave_JSON.json"

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
drop_objava_table = "DROP TABLE IF EXISTS objava;"
cur.execute(drop_objava_table)
conn.commit()

create_objava_table = '''CREATE TABLE objava
    (ID SERIAL PRIMARY KEY  NOT NULL,
    title                   TEXT,
    body                    TEXT,
    autor                   TEXT,
    autor_id                INTEGER,
    upvote                  INTEGER,
    downvote                INTEGER,
    visible                 BOOLEAN); '''
cur.execute(create_objava_table)
conn.commit()

objava_insert_query = """INSERT INTO objava 
    (title, body, autor,autor_id, upvote, downvote, visible) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

for key, value in objava_data.items():
    objava_values = (
        value["title"],
        value["body"],
        value["autor"],
        value["autor_id"],
        value["upvote"],
        value["downvote"],
        value["visible"]
    )
    cur.execute(objava_insert_query, objava_values)
    conn.commit()

cur.close()
conn.close()
