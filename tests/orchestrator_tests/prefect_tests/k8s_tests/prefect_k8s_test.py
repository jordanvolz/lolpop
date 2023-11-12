from typer.testing import CliRunner
from pathlib import Path
import os

from lolpop.cli.run import app as run_app
from lolpop.cli.package import app as package_app
from lolpop.utils import common_utils as utils

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.parent.resolve(
) / "examples/quickstart/classification/titanic/"
original_dir = os.getcwd()


def test_prefect_k8s_docker_image_packages_successfully():
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

    ## Provide valid arguments for the workflow command
    #result = runner.invoke(package_app, ["workflow", "QuickstartRunner",
    #                            "-m", "prefect_files.quickstart_runner",
    #                            "-c", "prefect_files/quickstart.yaml",
    #                            "--packager", "PrefectOrchestrator",
    #                            "--packaging-kwargs", '{"copy_files":["train.csv","test.csv", "process_titanic.py"], "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", "config_file":"prefect_files/quickstart.yaml"}'
    #                            ])

    output, exit_code = utils.execute_cmd(["lolpop", "package", "workflow", "QuickstartRunner",
                                           "-m", "prefect_files.quickstart_runner",
                                           "-c", "prefect_files/quickstart.yaml",
                                           "--packager", "PrefectOrchestrator",
                                           "--packaging-kwargs", '{"copy_files":["train.csv","test.csv", "process_titanic.py"], \
                                            "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", \
                                            "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, \
                                            "docker_image_tag":"lolpop-quickstartrunner-build-all-serve"}'
                                           ])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Packaging completed!" in output

    os.chdir(original_dir)


def test_prefect_k8s_runs_successfully():
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

    PREFECT_API_URL = f'PREFECT_API_URL={os.environ["PREFECT_API_URL"]}'
    PREFECT_API_KEY = f'PREFECT_API_KEY={os.environ["PREFECT_API_KEY"]}'
    output, exit_code = utils.execute_cmd(["kubectl", "apply", '-f', 'prefect_files/deployment-manifst.yaml'])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "deployment.apps/prefect-titanic created" in output


    output, exit_code = utils.execute_cmd("kubectl", "delete", "deployment", "prefect-titanic")

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert'deployment.apps "prefect-titanic" deleted'in output


    os.chdir(original_dir)

def test_k8s_deployment(): 
    pass