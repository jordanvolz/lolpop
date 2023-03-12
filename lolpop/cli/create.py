import typer 
from cookiecutter.main import cookiecutter 
from pathlib import Path
import os 

app = typer.Typer(help="Create new runners, piplines, and components.")

LOLPOP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PARENT_DIR = os.path.dirname(LOLPOP_DIR)

@app.command("component")
def component(
    component_type: str = typer.Argument(..., help="Component type (Should be snake_case)."),
    component_class: str = typer.Argument(..., help="Component class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        "%s/templates/component_template" % (PARENT_DIR), help="Path to the template file. Or a git url of a template file."),
    component_dir: Path = typer.Option("%s/component" %LOLPOP_DIR,
                                       help="Parent directory for the new component."),
): 
    create_template("component", component_type,
                    component_class, template_path, component_dir)
    
@app.command("pipeline")
def pipeline(
    pipeline_type: str = typer.Argument(..., help="Pipeline type (Should be snake_case)."),
    pipeline_class: str = typer.Argument(
        ..., help="Pipeline class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        "%s/templates/pipeline_template" % (PARENT_DIR), help="Path to the template file. Or a git url of a template file."),
    pipeline_dir: Path = typer.Option("%s/pipeline" % LOLPOP_DIR,
                                       help="Parent directory for the new pipeline."),
): 
    create_template("pipeline", pipeline_type,
                    pipeline_class, template_path, pipeline_dir)

@app.command("runner")
def runner(
    runner_type: str = typer.Argument(..., help="Component type (Should be snake_case)"),
    runner_class: str = typer.Argument(..., help="Component class name (Should be snake_case)."),
    template_path: str = typer.Argument(
        "%s/templates/runner_template" % (PARENT_DIR), help="Path to the template file. Or a git url of a template file."),
    runner_dir: Path = typer.Option("%s/runner" %LOLPOP_DIR,
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