import typer 
import click 
import os 

from lolpop.cli import create, run, package, test, datagen, seed 
from importlib.metadata import version
from typing import Optional
from pathlib import Path 
from cookiecutter.main import cookiecutter
from lolpop import __template_path__ as lolpop_template_path
from typer.core import TyperGroup 

try:
    __version__ = version("lolpop")
except:
    __version__ = "local-dev"

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()

app = typer.Typer(cls=NaturalOrderGroup,
                  help="lolpop: A software engineering framework for machine learning workflows.",
                  no_args_is_help=True)

app.add_typer(run.app, name="run")
app.add_typer(create.app, name="create")
app.add_typer(datagen.app, name="datagen")
app.add_typer(seed.app, name="seed")
app.add_typer(test.app, name="test")
app.add_typer(package.app, name="package")



def version_callback(value: bool):
    if value:
        try:
            typer.secho("lolpop version: %s" % __version__, fg="blue")
            raise typer.Exit()
        except Exception as e:
           raise typer.Exit()


@app.callback(context_settings=dict(help_option_names=["-h", "--help"]))
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print lolpop version",
    ),
):
    return True

@app.command("init", help="Initialize a lolpop project.")
def initialize(
    project_name: str = typer.Argument(..., help="Name of the project to create."), 
    project_path: Path = typer.Option(Path(os.getcwd()), help="Path to create project."), 
    template_path: str = typer.Option(
        lolpop_template_path + "/project_template", help="Path to the project template."),
    ): 
    try:
        cookiecutter(template=template_path,
                    extra_context={"project_name": project_name},
                    output_dir=project_path, no_input=True)
        typer.secho("Successfully created lolpop project %s at location %s/%s" %
                    (project_name, project_path, project_name), fg="green")
    except Exception as e: 
        typer.secho("Failed to create project %s: %s" %(project_name, str(e)), fg="red") 

@app.command("help", add_help_option=False, options_metavar="", hidden=True)
def help(ctx: typer.Context):
    """Show CLI usage help."""
    ctx.info_name = None
    typer.echo(ctx.parent.command.get_help(ctx))

if __name__ == "__main__":
    app()
