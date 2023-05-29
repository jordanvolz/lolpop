create table total_store_forecast_train as 
(select date, total_sales, type as holiday from 
(select date, 
sum(sales) as total_sales 
from stores_train 
group by date) 
left join (select * from stores_holidays_events where locale='National' and type='Holiday')
using (date)
order by date
)

create table total_store_forecast_test as 
(select date, type as holiday from 
(select date
from stores_test 
group by date) 
left join (select * from stores_holidays_events where locale='National' and type='Holiday')
using (date)
order by date
)