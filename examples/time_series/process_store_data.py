import pandas as pd
import numpy as np


def transform(data, **kwargs):
    expected_data = set(["train", "stores", "oil", "transactions", "holidays_events"])

    if len(expected_data.intersection(set(data.keys()))) < 5: 
        raise Exception("Not all datasets found. Expected: %s, Found: %s" %(expected_data, data.keys()))
    
    holidays=data.get("holidays_events").rename(columns={'type':'holiday_type'})
    df = data.get("train").merge(data.get("stores"), on="store_nbr").merge(
        data.get("oil"), on="date", how="left").merge(holidays, on="date", how="left").merge(
        data.get("transactions"), on=["date", "store_nbr"])


    return df
