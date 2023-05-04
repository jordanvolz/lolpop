import typer 
from lolpop.utils import common_utils as utils
from pathlib import Path
import os 
import json
import pandas as pd 

app = typer.Typer(help="Upload local data into your data platform. ")

LOLPOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#PARENT_DIR = os.path.dirname(LOLPOP_DIR)


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
    data_loader_class: str = typer.Option(
        "SnowflakeDataTransformer", "--data-loader-class", "-c", help="Data Loader class name."),
    dataloader_kwargs: str = typer.Option("{}", "--kwargs", "-k", 
                                          help="Keyword arguments (as a string) to pass into the data loader."),
):
    typer.secho("Loading data loader class %s" % data_loader_class, fg="blue")
    data_loader_cl = utils.load_class(data_loader_class, "component")
    logger_cl = utils.load_class("StdOutLogger", "component")
    data_loader = data_loader_cl(conf={}, pipeline_conf={}, runner_conf={}, components={"logger": logger_cl()}, **json.loads(dataloader_kwargs))
    data_loader.suppress_logger = True
    data_loader.suppress_notifier = True
    typer.secho("Successfully loaded data loader class %s" %
                data_loader_cl, fg="green")

    typer.secho("Begin saving file %s with data loader" %
                source_file, fg="blue")
    data = utils.create_df_from_file(source_file)
    data_loader.save_data(data, target)
    typer.secho("Successfully saved data to %s!" %target, fg="green")