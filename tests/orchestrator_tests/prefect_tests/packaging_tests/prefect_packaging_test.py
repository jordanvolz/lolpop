from pathlib import Path
import os

from lolpop.utils import common_utils as utils

example_dir = Path(__file__).parent.parent.parent.parent.parent.resolve(
) / "examples/quickstart/classification/titanic/"
original_dir = os.getcwd()


def test_prefect_docker_image_packages_successfully():
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["lolpop", "deployment", "package", "QuickstartRunner",
                                           "-m", "prefect_files.quickstart_runner",
                                           "-c", "prefect_files/quickstart.yaml",
                                           "--packager", "PrefectOrchestrator",
                                           "--packaging-kwargs", '{"copy_files":["train.csv","test.csv", "process_titanic.py"], \
                                            "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", \
                                            "config_file":"prefect_files/quickstart.yaml", "skip_validation":true}'
                                           ])

    # Assert that the command exits with a 0 status code
    assert exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Packaging completed!" in output

    os.chdir(original_dir)

def test_prefect_docker_image_packages_successfully_for_serve():
    os.chdir(example_dir)

    output, exit_code = utils.execute_cmd(["lolpop", "deployment", "package", "QuickstartRunner",
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

    def test_prefect_skipping_docker_build(): 
        os.chdir(example_dir)

        output, exit_code = utils.execute_cmd(["lolpop", "deployment", "package", "QuickstartRunner",
                                            "-m", "prefect_files.quickstart_runner",
                                            "-c", "prefect_files/quickstart.yaml",
                                            "--packager", "PrefectOrchestrator",
                                            "--packaging-kwargs", '{"work_pool": "test_work_pool", "copy_files":["train.csv","test.csv", "process_titanic.py"], \
                                                "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", \
                                                "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, \
                                                "docker_image_tag":"lolpop-quickstartrunner-build-all-delete-me"}'
                                            ])

        # Assert that the command exits with a 0 status code
        assert exit_code == 0
        # Assert that the expected success message is present in the output
        assert "Skipping docker build" in output

        os.chdir(original_dir)
