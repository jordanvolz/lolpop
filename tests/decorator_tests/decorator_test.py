
from pathlib import Path
import sys


parent_dir = Path(__file__).parent.resolve()
decorator_files = "%s/test_decorator_files" % parent_dir
sys.path.append(decorator_files)

#need to import after appending to syspath or it won't find the extension properly
from lolpop.runner import ClassificationRunner
config = "%s/showmanship.yaml" % decorator_files
runner = ClassificationRunner(conf=config, skip_config_validation=True)

def test_workflow_runs_successfully():

    out = runner.process.data_transformer.transform("train_data")
    assert out == "You're at your best when when the going gets rough. You've been put to the test, but it's never enough. You got the touch! You got the power! When all hell's breaking loose you'll be riding the eye of the storm. You got the heart! You got the motion! You know that when things get too tough, you got the touch!"

    out = runner.train.model_trainer.fit("train_data")
    assert out == "You're at your best when when the going gets rough. You've been put to the test, but it's never enough. You got the touch! You got the power! When all hell's breaking loose you'll be riding the eye of the storm. You got the heart! You got the motion! You know that when things get too tough, you got the touch!"

def test_default_component_skipped(): 
    out = runner.log("something")
    assert out == None 

def test_pipeline_skipped(): 
    try: 
        runner.process_data("train_data")
        assert False 
    except: 
        #this should fail, as we didn't decorate pipelines and we didn't provide 
        #enough of a config to run a real worflows
        assert True
