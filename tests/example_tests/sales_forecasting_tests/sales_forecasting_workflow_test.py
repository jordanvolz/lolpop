from typer.testing import CliRunner
from pathlib import Path
import os

from lolpop.cli.run import app

runner = CliRunner()

example_dir = Path(__file__).parent.parent.parent.parent.resolve(
) / "examples/quickstart/timeseries/sales_forecasting/"
original_dir = os.getcwd()


def test_sales_forecasting_workflow_runs_successfully():
    os.chdir(example_dir)

    # always end the mlflow run. We do this in case another process errored and failed 
    # to end the active run.
    import mlflow 
    mlflow.end_run()
    
    # Provide valid arguments for the workflow command
    result = runner.invoke(app, ["workflow", "QuickstartTimeSeriesRunner",
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
