import typer 
import inspect 
import os
import json 

from typing import List
from cookiecutter.main import cookiecutter
from pathlib import Path
from typer.core import TyperGroup

from lolpop import __template_path__ as lolpop_template_path
from lolpop.utils import common_utils as utils


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls = NaturalOrderGroup, help="Create new runners, piplines, and components.")

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
    extension_name: str = typer.Argument(None, help = "Name of the parent extension for this resource."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/component_template", help="Path to the template file. Or a git url of a template file."),
    project_dir: Path = typer.Option(os.getcwd(), help="Project directory for the new component."),
): 
    create_template("component", component_type,
                    component_class, template_path, project_dir, extension_name)
    

@app.command("pipeline", help="Initialize a custom pipeline.")
def pipeline(
    pipeline_type: str = typer.Argument(..., help="Pipeline type (Should be snake_case)."),
    pipeline_class: str = typer.Argument(
        ..., help="Pipeline class name (Should be snake_case)."),
    extension_name: str = typer.Argument(
            None, help="Name of the parent extension for this resource."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/pipeline_template", help="Path to the template file. Or a git url of a template file."),
    project_dir: Path = typer.Option(os.getcwd(), help="Parent directory for the new pipeline."),
): 
    create_template("pipeline", pipeline_type,
                    pipeline_class, template_path, project_dir, extension_name)


@app.command("runner", help="Initialize a custom component.")
def runner(
    runner_type: str = typer.Argument(..., help="Component type (Should be snake_case)"),
    runner_class: str = typer.Argument(..., help="Component class name (Should be snake_case)."),
    extension_name: str = typer.Argument(None, help="Name of the parent extension for this resource."),
    template_path: str = typer.Argument(
        lolpop_template_path + "/runner_template", help="Path to the template file. Or a git url of a template file."),
    project_dir: Path = typer.Option(os.getcwd(), help="Parent directory for the new component."),
): 
    create_template("runner", runner_type,
                    runner_class, template_path, project_dir, extension_name)
    
#template type = component, pipeline, runner, 
def create_template(template_type, object_type, object_class, template_path, project_dir, extension_name): 
    typer.secho("Creating template for %s %s" %(template_type, object_class), fg="blue")
    try: 
        object_class_camel = ''.join([i.title() for i in object_class.split("_")])
        object_type_camel = ''.join([i.title() for i in object_type.split("_")])
        #TODO: Check if object_type already exists and just copy a new template in that 
        #directory instead of trying to create a new folder
        output_dir = "%s/lolpop/extension/%s/%s" %(project_dir, extension_name, template_type)
        cookiecutter(template = template_path,
                    extra_context={
                        "%sClass" %template_type.title(): object_class_camel,
                        "%s_class" %template_type: object_class,
                        "%s_type" %template_type: object_type, 
                        "%sType" %template_type.title(): object_type_camel,
                        },
                    output_dir=output_dir, no_input=True)
        typer.secho("Successfully created template at location %s" %
                    output_dir, fg="green")
    except Exception as e: 
        typer.secho("Failed to create template for %s %s: %s" %(template_type, object_class, str(e)), fg="red") 


@app.command("documentation", help="Create documentation for a class.")
def create_documentation(
    source_file: Path = typer.Argument(
        ..., help="Path to the source file."),
    class_name: str = typer.Option(
        None, "--class-name", "-c", help="Class name in source_file to document."),
    method_filter: List[str] = typer.Option([], "--method-filter", "-f", help="Methods to include in the documentation. default=all."),
    generator_class: str = typer.Option(
        "OpenAIChatbot", "--generator-class", "-g", help="Generative AI Chatbot class name."),
    generator_kwargs: str = typer.Option(
        "{}", "--kwargs", "-k", help="Keyword arguments to pass into the generator class"),
    output_path: Path = typer.Option(None, "--output-path", "-o", help="The location to save the documentation"),
):
    chatbot = load_chatbot(generator_class)
    class_code, num_lines = get_source_from_file(source_file, class_name)

    if num_lines > 0: 
        typer.secho("Preparing prompt for chatbot...", fg="blue")
        messages=[]
        messages.append(chatbot.prepare_message(role="system", content="You are a technical writer for a software company."))
        filter_text = "this class"
        if len(method_filter)>0: 
            filter_text = "these methods in the class: %s" %str(method_filter)
        messages.append(chatbot.prepare_message(role="user", content="The following is a python class. I would like you to write technical documentation for %s. Include a description of each method in the class, as well as providing at least one example of using the class in a small code snippet. Please write your documentation in markdown format. Class Code: %s" %(filter_text,class_code)))
        typer.secho("Prompting chatbot and awaiting a response ...", fg="blue")
        response = chatbot.ask(messages=messages, **json.loads(generator_kwargs))
        typer.secho("Successfully queried chatbot. Received response: \n\n %s" %response, fg="green")

        if output_path: 
            with open(output_path, "w+") as f: 
                f.write(response)
            typer.secho("Successfully wrote response out to file %s" %output_path)

    else: 
        typer.secho("No lines found for class %s, aborting. Please check your inputs and try again." %class_name)


@app.command("tests", help="Create tests for a class.")
def create_tests(
    source_file: Path = typer.Argument(
        ..., help="Path to the source file."),
    class_name: str = typer.Option(
        None, "--class-name", "-c", help="Class name in source_file to document."),
    method_filter: List[str] = typer.Option(
        [], "--method-filter", "-f", help="Methods to include in the documentation. default=all."),
    generator_class: str = typer.Option(
        "OpenAIChatbot", "--generator-class", "-g", help="Generative AI Chatbot class name."),
    generator_kwargs: str = typer.Option(
        "{}", "--kwargs", "-k", help="Keyword arguments to pass into the generator class"),
    output_path: Path = typer.Option(
        None, "--output-path", "-o", help="The location to save the documentation"),
    testing_framework: str = typer.Option("pytest", "--testing-framework", "-t", help="The testing framework you would like the tests to be written in.")
):
    chatbot = load_chatbot(generator_class)
    class_code, num_lines = get_source_from_file(source_file, class_name)
    
    if num_lines > 0:
        typer.secho("Preparing prompt for chatbot...", fg="blue")
        messages = []
        messages.append(chatbot.prepare_message(
            role="system", content="You are an expert software developer for a software company."))
        filter_text = "all methods in this class"
        if len(method_filter) > 0:
            filter_text = "these methods in the class: %s" % str(
                method_filter)
        messages.append(chatbot.prepare_message(role="user", content="The following is a python class. I would like you to write tests for %s. Use the %s testing framework and python to write your tests. Please write at least two tests for each method and respond in the form of a python file. Class Code: %s" % (filter_text, testing_framework, class_code)))
        typer.secho("Prompting chatbot and awaiting a response ...", fg="blue")
        response = chatbot.ask(messages=messages, **
                               json.loads(generator_kwargs))
        typer.secho(
            "Successfully queried chatbot. Received response: \n\n %s" % response, fg="green")

        if output_path:
            with open(output_path, "w+") as f:
                f.write(response)
            typer.secho("Successfully wrote response out to file %s" %
                        output_path)

    else:
        typer.secho(
            "No lines found for class %s, aborting. Please check your inputs and try again." % class_name)


@app.command("docstrings", help="Create docstrings for a class.")
def create_docstrings(
    source_file: Path = typer.Argument(
        ..., help="Path to the source file."),
    class_name: str = typer.Option(
        None, "--class-name", "-c", help="Class name in source_file to document."),
    method_filter: List[str] = typer.Option(
        [], "--method-filter", "-f", help="Methods to include in the documentation. default=all."),
    generator_class: str = typer.Option(
        "OpenAIChatbot", "--generator-class", "-g", help="Generative AI Chatbot class name."),
    generator_kwargs: str = typer.Option(
        "{}", "--kwargs", "-k", help="Keyword arguments to pass into the generator class"),
    output_path: Path = typer.Option(
        None, "--output-path", "-o", help="The location to save the documentation")
    ):
    chatbot = load_chatbot(generator_class)
    class_code, num_lines = get_source_from_file(source_file, class_name)

    if num_lines > 0:
        typer.secho("Preparing prompt for chatbot...", fg="blue")
        messages = []
        messages.append(chatbot.prepare_message(
            role="system", content="You are an expert software developer for a software company."))
        filter_text = "all methods in this class"
        if len(method_filter) > 0:
            filter_text = "these methods in the class: %s" % str(
                method_filter)
        messages.append(chatbot.prepare_message(role="user", content="The following is a python class. I would like you to write docstrings for %s following Google's python guide. Be sure to include descriptios of all inputs (along with default values) and outputs, as well as a description of what each method does.  Class Code: %s" % (filter_text, class_code)))
        typer.secho("Prompting chatbot and awaiting a response ...", fg="blue")
        response = chatbot.ask(messages=messages, **
                               json.loads(generator_kwargs))
        typer.secho(
            "Successfully queried chatbot. Received response: \n\n %s" % response, fg="green")

        if output_path:
            with open(output_path, "w+") as f:
                f.write(response)
            typer.secho("Successfully wrote response out to file %s" %
                        output_path)

    else:
        typer.secho(
            "No lines found for class %s, aborting. Please check your inputs and try again." % class_name)



def load_chatbot(generator_class):
    typer.secho("Loading generator class %s..." % generator_class, fg="blue")
    generator_cl = utils.load_class(generator_class, "component")
    logger_cl = utils.load_class("StdOutLogger", "component")
    chatbot = generator_cl(components={"logger": logger_cl()})
    #suppress logging/notifying to reduce cli noise 
    chatbot.suppress_logger = True
    chatbot.suppress_notifier = True
    typer.secho("Successfully loaded generator class %s" %
                generator_class, fg="green")
    return chatbot 

def get_source_from_file(source_file, class_name): 
    typer.secho("Loading class %s from file %s and reading source code..." %
                (class_name, source_file), fg="blue")
    mod = utils.load_module_from_file(source_file)
    class_code = inspect.getsource(getattr(mod, class_name))
    num_lines = class_code.count("\n")
    typer.secho("Successfully loaded class %s! Found %s lines of code" %(class_name, num_lines), fg="green")

    return class_code, num_lines
