from typer.testing import CliRunner
from pathlib import Path
from omegaconf import OmegaConf
import os


from lolpop.cli.run import app

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.resolve(
) / "examples/classification/petfinder/"
original_dir = os.getcwd()


def test_dev_workflow_runs_successfully(tmp_dir):
    os.chdir(example_dir)
    # Provide valid arguments for the workflow command
    config = OmegaConf.load("dev.yaml")
    config.config["disable_git_commit"] = True
    file_path = tmp_dir / "dev.yaml"
    OmegaConf.save(config, file_path)
    result = runner.invoke(app, ["workflow", "ClassificationRunner",
                                 "--config-file", "%s" %file_path,
                                 "--build-method", "build_all"
                                 ])

    # Assert that the command exits with a 0 status code
    assert result.exit_code == 0
    # Assert that the expected success message is present in the output
    assert "Workflow completed!" in result.output

    os.chdir(original_dir)
