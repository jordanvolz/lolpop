import typer 
from cookiecutter.main import cookiecutter 
from pathlib import Path
import os 
from lolpop import __template_path__ as lolpop_template_path

app = typer.Typer(help="Create new runners, piplines, and components.")

LOLPOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#PARENT_DIR = os.path.dirname(LOLPOP_DIR)


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))


@app.command("component", help="Initialize a custom component.")
def component(
    component_type: str = typer.Argument(..., help="Component type (Should be snake_case)."),
    component_class: str = typer.Argument(..., help="Component class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/component_template", help="Path to the template file. Or a git url of a template file."),
    component_dir: Path = typer.Option(os.getcwd() + "/extension/component",
                                       help="Parent directory for the new component."),
): 
    create_template("component", component_type,
                    component_class, template_path, component_dir)
    

@app.command("pipeline", help="Initialize a custom pipeline.")
def pipeline(
    pipeline_type: str = typer.Argument(..., help="Pipeline type (Should be snake_case)."),
    pipeline_class: str = typer.Argument(
        ..., help="Pipeline class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/pipeline_template", help="Path to the template file. Or a git url of a template file."),
    pipeline_dir: Path = typer.Option(os.getcwd() + "/extention/pipeline",
                                       help="Parent directory for the new pipeline."),
): 
    create_template("pipeline", pipeline_type,
                    pipeline_class, template_path, pipeline_dir)


@app.command("runner", help="Initialize a custom component.")
def runner(
    runner_type: str = typer.Argument(..., help="Component type (Should be snake_case)"),
    runner_class: str = typer.Argument(..., help="Component class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/runner_template", help="Path to the template file. Or a git url of a template file."),
    runner_dir: Path = typer.Option(os.getcwd() + "/extension/runner",
                                       help="Parent directory for the new component."),
): 
    create_template("runner", runner_type,
                    runner_class, template_path, runner_dir)
    
#template type = component, pipeline, runner, 
def create_template(template_type, object_type, object_class, template_path, object_dir): 
    typer.secho("Creating template for %s %s" %(template_type, object_class), fg="blue")
    try: 
        object_class_camel = ''.join([i.title() for i in object_class.split("_")])
        object_type_camel = ''.join([i.title() for i in object_type.split("_")])
        #TODO: Check if object_type already exists and just copy a new template in that 
        #directory instead of trying to create a new folder
        cookiecutter(template = template_path,
                    extra_context={
                        "%sClass" %template_type.title(): object_class_camel,
                        "%s_class" %template_type: object_class,
                        "%s_type" %template_type: object_type, 
                        "%sType" %template_type.title(): object_type_camel,
                        },
                    output_dir=object_dir, no_input=True)
        typer.secho("Successfully created template at location %s" %object_dir, fg="green")
    except Exception as e: 
        typer.secho("Failed to create template for %s %s: %s" %(template_type, object_class, str(e)), fg="red") 