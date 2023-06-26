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
    runner_class: str = typer.Argument(..., help="Runner class."),
    test_config: Path = typer.Argument(..., help="Location of the testing configuration file."),
    runner_config: Path = typer.Option(None, help="Location of runner configuration file. Optional. If not provided, lolpop will attempt to use the testing configurationa as the runner configuration as well."),
    build_method: str = typer.Option("main",
                                     help="The method in the runner class to execute."),
    build_args: List[str] = typer.Option([], help="List of args to pass into build_method."),
    build_kwargs: str = typer.Option("{}", help="Dict (as a string) of kwargs to pass into build_method"),
): 

    #load class
    typer.secho("Loading runner %s" %runner_class, fg="blue")
    runner_cl = utils.load_class(runner_class, class_type="runner")
    typer.secho("Loaded %s!" %runner_class, fg="green")

    #build testing plan 
    typer.secho("Constructing test plan from configuration: %s" %test_config, fg="blue")
    test_plan, test_logger = utils.generate_test_plan(test_config)
    typer.secho("Test plan built! Found %s instructions" %len(test_plan), fg="green")

    #intantiate class 
    if runner_config is None: 
        runner_config = test_config
    typer.secho("Initializing class %s with config file %s" %(runner_class, runner_config), fg="blue")
    runner = runner_cl(conf=runner_config)
    typer.secho("Initialized!", fg="green")

    #apply test plan to class
    typer.secho("Applying test plan to class %s" %(runner_class), fg="blue")
    runner = utils.apply_test_plan(runner, test_plan, test_logger)
    typer.secho("Test plan applied!", fg="green")

    if hasattr(runner, build_method): 
        typer.secho("Executing %s.%s with args %s and kwargs %s" %(runner_class, build_method, build_args, build_kwargs), fg="blue")
        func = getattr(runner, build_method)
        func(*build_args, **json.loads(build_kwargs))
        typer.secho("Workflow completed!", fg="green")        
    else: 
        typer.secho("ERROR: Method %s not found in class %s!" %(build_method, runner_class), fg="red")