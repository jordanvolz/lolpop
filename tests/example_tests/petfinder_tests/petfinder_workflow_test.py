from typer.testing import CliRunner
from pathlib import Path
from omegaconf import OmegaConf
import os
from lolpop.utils import common_utils as utils

from lolpop.cli.run import app

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.resolve(
) / "examples/classification/petfinder/"
original_dir = os.getcwd()


def test_petfinder_dev_workflow_runs_successfully(tmp_path):
    os.chdir(example_dir)
    
    # always end the mlflow run. We do this in case another process errored and failed
    # to end the active run.
    try:
        import mlflow
        mlflow.set_tracking_uri("./mlruns")
        mlflow.end_run()
        mlflow.end_run()
    except:
        pass

    #change config to disable commits so we don't commit stuff into the main branch. 
    config = OmegaConf.load("dev.yaml")
    rvc_conf = config.get("resource_version_control", OmegaConf.create({"config": {}}))
    rvc_conf.config["disable_git_commit"] = True 
    rvc_conf.config["git_path_to_dvc_dir"] = "examples/classification/petfinder"
    config["resource_version_control"] = rvc_conf
    #dvc is set up as a subdir, i.e dvc init --subdir, so we have to provide the path to the dvc dir 
    #so that git commits will work
    file_path = tmp_path / "dev.yaml" #tmp_path gets automatically cleaned up by pytest
    OmegaConf.save(config, file_path)

    #run workflow! 
    result = runner.invoke(app, ["workflow", "ClassificationRunner",
                                 "--config-file", "%s" %file_path,
                                 "--build-method", "build_all"
                                 ])


    # Assert that the command exits with a 0 status code
    assert result.exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in result.output

    os.chdir(original_dir)

    os.environ["SKIP_DATA"] = "true"
    utils.execute_cmd(["make", "clean_example_petfinder"])
    utils.execute_cmd(["make", "example_petfinder"])
