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

PREFECT_API_URL = f'PREFECT_API_URL={os.environ["PREFECT_API_URL"]}'
PREFECT_API_KEY = f'PREFECT_API_KEY={os.environ["PREFECT_API_KEY"]}'

def test_prefect_docker_runs_successfully():
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["docker", "run", '-e', PREFECT_API_URL,
                      '-e', PREFECT_API_KEY, 'lolpop-quickstartrunner-build-all'])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in output

    os.chdir(original_dir)

def test_docker_deployment_runs_successfully(): 
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["lolpop", "deployment", 'run', "prefect-entrypoint/lolpop-quickstartrunner-build_all",
                      '-c', "prefect_files/quickstart.yaml", '--deployer', "PrefectOrchestrator"])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Deployment ran!" in output

    os.chdir(original_dir)