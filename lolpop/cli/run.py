import typer 
from pathlib import Path 
from lolpop.utils import common_utils as utils
from typing import List
import json
from typer.core import TyperGroup


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls = NaturalOrderGroup, help="Run workflows with lolpop.")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))

@app.command("workflow", help="Run a workflow.")
def workflow(
    runner_class: str = typer.Argument(..., help="Runner class."),
    config_file: Path = typer.Option(..., "-c", "--config-file", help="Location of runner configuration file."),
    build_method: str = typer.Option("main", "-b", "--build-method",
                                       help="The method in the runner class to execute."),
    build_args: List[str] = typer.Option([], help="List of args to pass into build_method."),
    build_kwargs: str = typer.Option("{}", help="Dict (as a string) of kwargs to pass into build_method"),
    local_file: Path = typer.Option(None, "-l", "--local-file", help="Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. "),
    skip_validation: bool = typer.Option(False, "--skip-validation", help="Skip configuration validation.")
): 

    plugin_mods = []
    if local_file is not None: 
        cl = utils.load_module_from_file(local_file)
        plugin_mods = [cl.__name__]
    typer.secho("Loading class %s" %runner_class, fg="blue")
    runner_cl = utils.load_class(runner_class, plugin_mods=plugin_mods, class_type="runner")
    if runner_cl is None: 
        typer.secho("Failed to properly load class %s. Exiting..." %runner_class, fg="red")
        raise typer.Exit(code=1)
    typer.secho("Loaded %s!" %runner_class, fg="green")

    typer.secho("Initializing class %s with config file %s" %(runner_class, config_file), fg="blue")
    runner = runner_cl(conf=config_file, skip_config_validation=skip_validation)
    typer.secho("Initialized!", fg="green")
    
    if hasattr(runner, build_method): 
        typer.secho("Executing %s.%s with args %s and kwargs %s" %(runner_class, build_method, build_args, build_kwargs), fg="blue")
        func = getattr(runner, build_method)
        func(*build_args, **json.loads(build_kwargs))
        typer.secho("Workflow completed!", fg="green")        
    else: 
        typer.secho("ERROR: Method %s not found in class %s!" %(build_method, runner_class), fg="red")