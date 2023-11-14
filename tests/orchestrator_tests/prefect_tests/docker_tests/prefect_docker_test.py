from typer.testing import CliRunner
from pathlib import Path
import os

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

def test_docker_deployment_builds_successfully(): 
    os.chdir(example_dir)


    output, exit_code = utils.execute_cmd(["lolpop", "deployment", 'build',
                                        '-c', "prefect_files/quickstart.yaml",
                                        '--deployer', "PrefectOrchestrator", 
                                        "--deployment-kwargs", '{ "work_pool":"lolpop-docker-pool", "flow_class":"prefect_files.run", "flow_entrypoint": "prefect_entrypoint","docker_image_name":"lolpop-quickstartrunner-build-all", "job_variables":{"image_pull_policy":"Never"}}',
                                        "-n", 'lolpop-quickstartrunner-build-all-docker',  "-l", "prefect_files/run.py"])
    

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Deployment completed!" in output

    os.chdir(original_dir)


def test_docker_deployment_runs_successfully():
    os.chdir(example_dir)


    output, exit_code = utils.execute_cmd(["lolpop", "deployment", 'run', 
                                           "prefect-entrypoint/lolpop-quickstartrunner-build-all-docker",
                                           '-c', "prefect_files/quickstart.yaml", 
                                           '--deployer', "PrefectOrchestrator"])


    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Deployment ran!" in output

    os.chdir(original_dir)