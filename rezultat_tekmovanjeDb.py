import json
import py2psql
import os
import psycopg2
import time
from datetime import datetime
#predstavlja posamezen nastop tekmovalca, poveže tekmovalca z tekmovanjem

conn = psycopg2.connect(
    host=py2psql.hostname,
    dbname=py2psql.database,
    user=py2psql.username,
    password=py2psql.pwd,
    port=py2psql.port_id)
cur = conn.cursor()

values = [
    (1, 1),
    (2, 2),
    (3, 1),
    (4, 3),
    (5, 2),
    (6, 1),
    (7, 4),
    (8, 3),
    (9, 2),
    (10, 1),
    (11, 5),
    (12, 4),
    (13, 3),
    (14, 2),
    (15, 1),
    (16, 1),
    (17, 3),
    (18, 2),
    (19, 1),
    (20, 4),
    (21, 3),
    (22, 2),
    (23, 1),
    (24, 5),
    (25, 4),
    (26, 3),
    (27, 2),
    (28, 1),
    (29, 1),
    (30, 3)
]


drop_objava_table = "DROP TABLE IF EXISTS rezultat_tekmovanje;"
cur.execute(drop_objava_table)
conn.commit()

create_rezultat_tekmovanje_table = '''CREATE TABLE rezultat_tekmovanje (
    ID SERIAL PRIMARY KEY NOT NULL,
    Rezultat_ID INTEGER,
    Tekmovanje_ID INTEGER
);'''
cur.execute(create_rezultat_tekmovanje_table)
conn.commit()

for values in values:
    insert_statement = "INSERT INTO rezultat_tekmovanje (Rezultat_ID, Tekmovanje_ID) VALUES (%s, %s);"
    cur.execute(insert_statement, values)
    conn.commit()

zacetek = time.time()
zacetekDatetime = datetime.fromtimestamp(zacetek).strftime('%Y-%m-%d %H:%M:%S')
print("zacetek : " + str(zacetekDatetime))

cur.close()
conn.close()
