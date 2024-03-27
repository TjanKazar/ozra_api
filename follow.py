import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
 
conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()

drop_objava_table = "DROP TABLE IF EXISTS follow;"
cur.execute(drop_objava_table)
conn.commit()

create_uporabnik_tekmovanje_table = '''CREATE TABLE follow (
    ID SERIAL PRIMARY KEY NOT NULL,
    follower INTEGER,
    followed INTEGER
);'''
cur.execute(create_uporabnik_tekmovanje_table)
conn.commit()

cur.close()
conn.close()
