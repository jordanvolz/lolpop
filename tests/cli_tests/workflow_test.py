import pytest
from typer.testing import CliRunner
from pathlib import Path

from lolpop.cli.test import app

runner = CliRunner()


def test_workflow_runs_successfully():
    # Provide valid arguments for the workflow command
    parent_dir = Path(__file__).parent.resolve()
    result = runner.invoke(app, ["workflow", "BaseModelTrainer", 
                                 "%s/test_workflow_files/test_conf.yaml" %parent_dir, 
                                 "--integration-type", "component",
                                 "--build-method", "fit", 
                                 "--build-args", "'data!'"])

    # Assert that the command exits with a 0 status code
    assert result.exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in result.output


def test_workflow_missing_arguments():
    # Provide incomplete arguments for the workflow command
    result = runner.invoke(app, ["workflow", "StdOutLogger"])

    # Assert that the command exits with a non-zero status code
    assert result.exit_code != 0
    # Assert that the expected error message is present in the output
    assert "Missing argument" in result.output
