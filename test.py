import time
import psycopg2
from psycopg2 import extras

conn = psycopg2.connect("dbname=postgres host=127.0.0.1 user=postgres password=postgres")
cur = conn.cursor()

cur.execute("DELETE FROM points")
cur.execute("DELETE FROM relations")

start = time.time()

raw_list = [[i,i] for i in range(2000000)]
query = "INSERT INTO points VALUES %s"
tuples_list =[tuple(ls) for  ls in raw_list]
extras.execute_values(cur, query, tuples_list)
conn.commit()

conn.commit()
raw_list = [[i,i,i+1] for i in range(2000000)]
query = "INSERT INTO relations VALUES %s"
tuples_list =[tuple(ls) for  ls in raw_list]
extras.execute_values(cur, query, tuples_list)
conn.commit()

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

cur.close()
conn.close()