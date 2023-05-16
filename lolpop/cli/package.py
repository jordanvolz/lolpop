import typer 

app = typer.Typer(help="Package a lolpop workflow.")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))
