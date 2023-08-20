import pytest 

@pytest.mark.skip(reason="not a pytest test")
def test(obj, data, *args, **kwargs):
    null_col = [] 
    for col in data.columns: 
        if data[col].isnull().all(): 
            null_col.append(col)
    if len(null_col) >0: 
        obj.log("Null column(s) found: %s" %(str(null_col)))
    return len(null_col)==0 
