import typer
from typer.core import TyperGroup
import lolpop.extension.cli as cli_extensions

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()


app = typer.Typer(cls=NaturalOrderGroup, help="Run lolpop CLI extensions.")

extensions = [x for x in dir(cli_extensions) if not x.startswith("_") and x != "typer"]
typer_extensions = []
for ext in extensions:
    ext_cl = getattr(cli_extensions, ext)
    for method in dir(ext_cl): 
        if isinstance(getattr(ext_cl, method), typer.main.Typer):
            typer_extensions.append((ext_cl, method))
for ext in typer_extensions:
    name = ext[0].__name__.split(".")[-1]
    app.add_typer(getattr(ext[0],ext[1]), name=name)
