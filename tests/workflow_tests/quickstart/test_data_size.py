import pytest 

@pytest.mark.skip(reason="not a pytest test")
def test(obj, data, *args, **kwargs): 
    return data.shape[0]>0