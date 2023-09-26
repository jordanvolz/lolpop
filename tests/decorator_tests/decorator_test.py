
from pathlib import Path
import sys

parent_dir = Path(__file__).parent.resolve()
decorator_files = "%s/test_decorator_files" % parent_dir
sys.path.append(decorator_files)


def test_workflow_runs_successfully():
    from lolpop.runner import ClassificationRunner
    config = "%s/showmanship.yaml" %decorator_files
    runner = ClassificationRunner(conf=config, skip_config_validation=True)

    out = runner.process.data_transformer.transform("train_data")
    assert out == "You're at your best when when the going gets rough. You've been put to the test, but it's never enough. You got the touch! You got the power! When all hell's breaking loose you'll be riding the eye of the storm. You got the heart! You got the motion! You know that when things get too tough, you got the touch!"

    out = runner.train.model_trainer.fit("train_data")
    assert out == "You're at your best when when the going gets rough. You've been put to the test, but it's never enough. You got the touch! You got the power! When all hell's breaking loose you'll be riding the eye of the storm. You got the heart! You got the motion! You know that when things get too tough, you got the touch!"

    out = runner.log("something")
    assert out == None 