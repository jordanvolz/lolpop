import duckdb
import os

if not os.path.exists("duckdb"):
    os.mkdir("duckdb")
con = duckdb.connect(database="duckdb/duck.db")

con.sql("CREATE or REPLACE TABLE stores_train as SELECT * FROM read_csv_auto('data/train.csv')")
con.sql("CREATE or REPLACE TABLE stores_test as SELECT * FROM read_csv_auto('data/test.csv')")
con.sql("CREATE or REPLACE TABLE stores_holiday_events as SELECT * FROM read_csv_auto('data/holidays_events.csv')")

con.sql("""create or replace table total_store_forecast_train as 
(select date, total_sales, type as holiday from 
(select date, 
sum(sales) as total_sales 
from stores_train 
group by date) 
left join (select * from stores_holiday_events where locale='National' and type='Holiday')
using (date)
order by date
)"""
        )
        
con.sql("""create or replace table total_store_forecast_test as 
(select date, type as holiday from 
(select date
from stores_test 
group by date) 
left join (select * from stores_holiday_events where locale='National' and type='Holiday')
using (date)
order by date)"""
        )

print(con.sql("show tables"))

print(con.sql("select * from total_store_forecast_train limit 5"))
print(con.sql("select * from total_store_forecast_test limit 5"))
