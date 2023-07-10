import typer
from typer.core import TyperGroup
import lolpop.cli.extensions as cli_extensions

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()


app = typer.Typer(cls=NaturalOrderGroup, help="Run lolpop CLI extensions.")

@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))

#get all extensions
extensions = [x for x in dir(cli_extensions) if not x.startswith("_") and x != "typer"]
for ext in extensions:
    ext_cl = getattr(cli_extensions, ext)
    #look for the typer entrypoint and add that here
    for method in dir(ext_cl): 
        if isinstance(getattr(ext_cl, method), typer.main.Typer):
            name = ext_cl.__name__.split(".")[-1].replace("_","-")
            app.add_typer(getattr(ext_cl, method), name=name)
    
