import typer
from typer.core import TyperGroup


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()


app = typer.Typer(cls=NaturalOrderGroup,
                  help="cli unit test")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))


@app.command("pop", help="This is the first command in the command group.")
def pop():
    print("pop!")
