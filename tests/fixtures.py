import pytest 
import pandas as pd 
import numpy as np 
import random 
from faker import Faker 
from lolpop.component import StdOutLogger, StdOutNotifier

fake = Faker() 


@pytest.fixture(scope="session")
def simple_data(): 
    return pd.DataFrame(create_rows_faker(10000))


@pytest.fixture(scope="session")
def simple_ts_data():
    data = pd.DataFrame({
        "date": pd.date_range(start='2022-01-01', periods=100, freq='D'),
        "value": np.random.normal(0, 1, 100)
    })
    return data

def create_rows_faker(num=1):
    output = [{"id": x,
               "name": fake.name(),
               "address": fake.address(),
               "email": fake.email(),
               "city": fake.city(),
               "state": fake.state(),
               "job": fake.job(),
               "date_time": fake.date_time(),
               "some_bool" :fake.boolean(),
               "some_float": fake.pyfloat(),
               "some_int": fake.pyint(), 
               "some_string":fake.pystr(),
               } for x in range(num)]
    return output

@pytest.fixture
def fake_component_config(tmp_path_factory):
    return {
        "conf": {
            "config": {
                "local_dir": str(tmp_path_factory.mktemp("pytest")),
            }
        },
        "problem_type" : "fake_problem",
        "component" : {
            "logger": StdOutLogger({}),
            "notifier": StdOutNotifier({}),
        },
    }

#def generate_required_conf(required_conf):
#    required_components = {}
#    components = required_conf.get("component",[])
#    for component in components: 
#        if "|" in component: 
#            component, required_class = component.split("|")
#        if required_class = None: 
#            required_class =
#    pass 

    