
from pathlib import Path
import sys

from typer.testing import CliRunner

runner = CliRunner()

parent_dir = Path(__file__).parent.resolve()
extension_files = "%s/test_extension_files" % parent_dir
sys.path.append(extension_files)

def test_workflow_runs_successfully():
    #need to set syspath before loadin extension module
    from lolpop.cli.extension import app
    # Provide valid arguments for the workflow command
    result = runner.invoke(app, ["lol", "pop"])

    # Assert that the command exits with a 0 status code
    assert result.exit_code == 0
    # Assert that the expected success message is present in the output
    assert "pop!" in result.output


def test_workflow_missing_command():
    sys.path.remove(extension_files)
    from lolpop.cli.extension import app
    # Provide incomplete arguments for the workflow command
    result = runner.invoke(app, ["pop"])

    # Assert that the command exits with a non-zero status code
    assert result.exit_code != 0
    # Assert that the expected error message is present in the output
    assert "No such command" in result.output
