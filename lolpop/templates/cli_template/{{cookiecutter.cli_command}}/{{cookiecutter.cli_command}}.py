import typer 
from typer.core import TyperGroup

class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls = NaturalOrderGroup, help="{{cookiecutter.command_description}}")

@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))

@app.command("my-first-command", help="This is the first command in the command group.")
def my_first_command(
    my_first_argument: str = typer.Argument(..., help="A description of this argument"),
    my_first_option: str = typer.Option(None, help="A description of this option."),
    my_second_option: str = typer.Option(None, help="A description of this option."),
): 
    #your code here 
    pass 


@app.command("my-second-command", help="This is the first second in the command group.")
def my_second_command(
    my_first_argument: str = typer.Argument(...,
                                            help="A description of this argument"),
    my_first_option: str = typer.Option(
        None, help="A description of this option."),
    my_second_option: str = typer.Option(
        None, help="A description of this option."),
):
    #your code here
    pass
