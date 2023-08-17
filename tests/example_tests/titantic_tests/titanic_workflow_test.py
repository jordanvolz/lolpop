from typer.testing import CliRunner
from pathlib import Path
import os 

from lolpop.cli.run import app

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.resolve() / "examples/quickstart/classification/titanic/"
original_dir = os.getcwd() 

def test_titanic_workflow_runs_successfully():
    os.chdir(example_dir)
    # Provide valid arguments for the workflow command
    result = runner.invoke(app, ["workflow", "QuickstartRunner",
                                 "--config-file", "quickstart.yaml",
                                 "--build-method", "build_all",
                                 "--local-file", "quickstart_runner.py",
                                 "--skip-validation"
                                ])

    # Assert that the command exits with a 0 status code
    assert result.exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in result.output

    os.chdir(original_dir)
