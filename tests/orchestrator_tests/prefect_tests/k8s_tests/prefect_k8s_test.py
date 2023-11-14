from typer.testing import CliRunner
from pathlib import Path
import os

from lolpop.utils import common_utils as utils

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.parent.resolve(
) / "examples/quickstart/classification/titanic/"
original_dir = os.getcwd()



def test_k8s_deployment_builds_successfully():
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["lolpop", "deployment", 'build',
                                           '-c', "prefect_files/quickstart.yaml",
                                           '--deployer', "PrefectOrchestrator",
                                           "--deployment-kwargs", '{"work_pool":"lolpop-k8s-pool", "flow_class":"prefect_files.run", "flow_entrypoint":"prefect_entrypoint", "docker_image_name":"lolpop-quickstartrunner-build-all", "job_variables":{"image_pull_policy":"Never", "namespace":"lolpop", "service_account": "lolpop-prefect-sa"}}',
                                           "-n", 'lolpop-quickstartrunner-build-all-k8s',  "-l", "prefect_files/run.py", 
                                           "-t", "kubernetes"])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Deployment completed!" in output

    os.chdir(original_dir)


def test_k8s_deployment_runs_successfully():
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["lolpop", "deployment", 'run',
                                           "prefect-entrypoint/lolpop-quickstartrunner-build-all-k8s",
                                           '-c', "prefect_files/quickstart.yaml",
                                           '--deployer', "PrefectOrchestrator"])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Deployment ran!" in output

    os.chdir(original_dir)
