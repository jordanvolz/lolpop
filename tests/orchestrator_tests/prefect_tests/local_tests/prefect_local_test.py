from typer.testing import CliRunner
from pathlib import Path
import os

from lolpop.cli.run import app as run_app
from lolpop.utils import common_utils as utils

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.parent.resolve(
) / "examples/quickstart/classification/titanic/"
original_dir = os.getcwd()


def test_prefect_local_runs_successfully():
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

    # You get a a strange error if you run this via the normal way w/ typer. Execute via execute_cmd instead
    ## Provide valid arguments for the workflow command
    #result = runner.invoke(run_app, ["workflow", "QuickstartRunner",
    #                            "--config-file", "prefect_files/quickstart.yaml",
    #                            "--build-method", "build_all",
    #                            "--local-file", "prefect_files/quickstart_runner.py",
    #                            "--skip-validation"
    #                            ])

    output, exit_code = utils.execute_cmd(["lolpop", "run", "workflow", "QuickstartRunner",
                                           "--config-file", "prefect_files/quickstart.yaml",
                                           "--build-method", "build_all",
                                           "--local-file", "prefect_files/quickstart_runner.py",
                                           "--skip-validation"])
    
    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in output
    # Assert "prefect" in output -- i.e. prefect was actually used 
    assert "prefect" in output

    os.chdir(original_dir)

def test_local_deployment_runs_successfully_with_no_prefect(): 
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

    # You get a a strange error if you run this via the normal way w/ typer. Execute via execute_cmd instead
    ## Provide valid arguments for the workflow command
    #result = runner.invoke(run_app, ["workflow", "QuickstartRunner",
    #                            "--config-file", "prefect_files/quickstart.yaml",
    #                            "--build-method", "build_all",
    #                            "--local-file", "prefect_files/quickstart_runner.py",
    #                            "--skip-validation"
    #                            ])

    output, exit_code = utils.execute_cmd(["lolpop", "run", "workflow", "QuickstartRunner",
                                           "--config-file", "quickstart.yaml",
                                           "--build-method", "build_all",
                                           "--local-file", "quickstart_runner.py",
                                           "--skip-validation"])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in output
    # Assert "prefect" not in output -- i.e. prefect was not actually used
    assert "prefect" not in output

    os.chdir(original_dir)
