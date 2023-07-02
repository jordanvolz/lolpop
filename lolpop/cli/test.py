import typer 
import json 
from typer.core import TyperGroup 
from pathlib import Path 
from typing import List 

from lolpop.utils import common_utils as utils

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls=NaturalOrderGroup, help="Test lolpop runners, pipelines, and components.")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))


@app.command("workflow", help="Test a workflow.")
def workflow(
    integration_class: str = typer.Argument(..., help="Integration class to test."),
    test_config: Path = typer.Argument(..., help="Location of the testing configuration file."),
    integration_config: Path = typer.Option(None, help="Location of integration configuration file. Optional. If not provided, lolpop will attempt to use the testing configurationa as the runner configuration as well."),
    integration_type: str = typer.Option("runner",
                                     help="The type of class to test: runner, pipeline, componenet, etc."),
    build_method: str = typer.Option("main",
                                     help="The method in the integration class to execute."),
    build_args: List[str] = typer.Option([], help="List of args to pass into build_method."),
    build_kwargs: str = typer.Option("{}", help="Dict (as a string) of kwargs to pass into build_method"),
): 
    #load class
    typer.secho("Loading integration %s" % integration_class, fg="blue")
    integration_cl = utils.load_class(
        integration_class, class_type=integration_type)
    typer.secho("Loaded %s!" % integration_class, fg="green")

    #build testing plan 
    typer.secho("Constructing test plan from configuration: %s" %test_config, fg="blue")
    test_plan, test_logger, test_recorder = utils.generate_test_plan(test_config)
    typer.secho("Test plan built! Found %s method(s) to test" %len(test_plan), fg="green")

    #intantiate class 
    if integration_config is None: 
        integration_config = test_config
    typer.secho("Initializing class %s with config file %s" %(integration_class, integration_config), fg="blue")
    integration = integration_cl(conf=integration_config)
    typer.secho("Initialized!", fg="green")

    #apply test plan to class
    typer.secho("Applying test plan to class %s" %(integration_class), fg="blue")
    integration = utils.apply_test_plan(integration, test_plan, test_recorder, test_logger)
    typer.secho("Test plan applied!", fg="green")

    if hasattr(integration, build_method):
        typer.secho("Executing %s.%s with args %s and kwargs %s" % (
            integration_class, build_method, build_args, build_kwargs), fg="blue")
        func = getattr(integration, build_method)
        func(*build_args, **json.loads(build_kwargs))
        typer.secho("Workflow completed!", fg="green")

        if test_recorder is not None: 
            typer.secho('\nPrinting Test Report: ', fg="blue")
            test_recorder.print_report()        
    else: 
        typer.secho("ERROR: Method %s not found in class %s!" %(build_method, integration_class), fg="red")