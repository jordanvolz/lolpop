import pytest 
import pandas as pd 
import random 
from faker import Faker 
from lolpop.component import StdOutLogger, StdOutNotifier

fake = Faker() 


@pytest.fixture(scope="session")
def simple_data(): 
    return pd.DataFrame(create_rows_faker(10000))


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
               "some_float": fake.pybool(),
               "some_int": fake.pyint(), 
               "some_string":fake.pystr(),
               } for x in range(num)]
    return output

@pytest.fixture
def fake_component_config(tmp_path_factory):
    return {
        "config": {
            "config": {
                "local_dir": str(tmp_path_factory.mktemp("pytest")),
            }
        },
        "pipeline_conf": {},
        "runner_conf" : {}, 
        "parent_process" : "fake_parent", 
        "problem_type" : "fake_problem",
        "components" : {
            "logger": StdOutLogger({}),
            "notifier": StdOutNotifier({}),
        },
    }

#def generate_required_conf(required_conf):
#    required_components = {}
#    components = required_conf.get("components",[])
#    for component in components: 
#        if "|" in component: 
#            component, required_class = component.split("|")
#        if required_class = None: 
#            required_class =
#    pass 

    