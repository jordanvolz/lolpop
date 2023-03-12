import typer 
import click 

from lolpop.cli import create, run, package, test 
from importlib.metadata import version
from typing import Optional

try:
    __version__ = version("lolpop")
except:
    __version__ = "local-dev"

class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()

app = typer.Typer(cls=NaturalOrderGroup,
                  help="lolpop: A software engineering framework for machine learning workflows.",
                  no_args_is_help=True)

app.add_typer(run.app, name="run")
app.add_typer(create.app, name="create")
app.add_typer(test.app, name="test")
app.add_typer(package.app, name="package")


def version_callback(value: bool):
    if value:
        try:
            typer.secho(f"lolpop version: %s" %__version__, fg="blue")
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
    return


@app.command("help", add_help_option=False, options_metavar="")
def help(ctx: typer.Context):
    """Show CLI usage help."""
    ctx.info_name = None
    typer.echo(ctx.parent.command.get_help(ctx))

if __name__ == "__main__":
    app()
