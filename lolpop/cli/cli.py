import typer 
import os 
import re 

from lolpop.cli import create, run, test, datagen, seed, extension, deployment
from importlib.metadata import version
from typing import Optional
from pathlib import Path 
from cookiecutter.main import cookiecutter
from lolpop import __template_path__ as lolpop_template_path
from typer.core import TyperGroup 
from importlib.metadata import metadata
from collections import defaultdict
from pprint import pprint

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
app.add_typer(deployment.app, name="deployment")
app.add_typer(extension.app, name="extension")

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


@app.command("list-extras", help="list available extra packages")
def list_extras(
    package_name: str = typer.Option("lolpop",
                                       help="Name of package to list available extras for."),
    print_reqs: bool = typer.Option(False, "--print-reqs", help="Print depencencies included in the extra packages.")
):
    extras = metadata(package_name).get_all("Provides-Extra")
    required_dists = metadata(package_name).get_all("Requires-Dist")

    result = defaultdict(list)
    for extra in extras:
        for required_dist in required_dists:
            suffix = f'extra == "{extra}"'
            if suffix in required_dist:
                result[extra].append(re.sub(r";.+", "", required_dist))

    for k, v in result.items():
        typer.secho(k, fg="blue")
        if print_reqs: 
            for req in v: 
                typer.secho(req, fg="yellow")

    typer.secho("\nTo install all extras, you can issue the following command:", fg="green") 
    typer.secho("pip3 install 'lolpop[%s]'" %",".join(result.keys()))


if __name__ == "__main__":
    app()
