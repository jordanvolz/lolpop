import duckdb 
import os 

if not os.path.exists("duckdb"): 
    os.mkdir("duckdb")
con = duckdb.connect(database="duckdb/duck.db")

con.sql("CREATE or REPLACE TABLE crab_train as SELECT * FROM read_csv_auto('data/train.csv')")
con.sql("CREATE or REPLACE TABLE crab_test as SELECT * FROM read_csv_auto('data/test.csv')")

print(con.sql("show tables"))

print(con.sql("select * from crab_train limit 5"))
print(con.sql("select * from crab_test limit 5"))

