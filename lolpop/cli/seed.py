import typer 
from lolpop.utils import common_utils as utils
from pathlib import Path
import os 
import json
import pandas as pd 
from typer.core import TyperGroup 

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    

app = typer.Typer(cls = NaturalOrderGroup, help="Upload local data into your data platform. ")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))

@app.command("file", help="Seed a file.")
def seed_file(
    source_file: Path = typer.Argument(
        ..., help="Path to the source file"),
    target: str = typer.Argument(
        ..., help="Where the data is going. Should be a table in DW or path in the object store, etc."),
    data_connector_class: str = typer.Option(None, "--data-connector-class", "-c", help="Data Connector class name."),
    data_connector_kwargs: str = typer.Option("{}", "--kwargs", "-k", 
                                          help="Keyword arguments (as a string) to pass into the data connector."),
):
    typer.secho("Loading data connector class %s" % data_connector_class, fg="blue")
    data_connector_cl = utils.load_class(data_connector_class, "component")
    logger_cl = utils.load_class("StdOutLogger", "component")
    data_connector = data_connector_cl(conf={}, pipeline_conf={}, runner_conf={}, components={
                                       "logger": logger_cl()}, **json.loads(data_connector_kwargs))
    data_connector.suppress_logger = True
    data_connector.suppress_notifier = True
    typer.secho("Successfully loaded data connector class %s" %
                data_connector_cl, fg="green")

    typer.secho("Begin saving file %s with data connector" %
                source_file, fg="blue")
    data = utils.create_df_from_file(source_file)
    data_connector.save_data(data, target)
    typer.secho("Successfully saved data to %s!" %target, fg="green")