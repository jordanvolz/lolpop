import typer 
from typer.core import TyperGroup
from typing import List
from pathlib import Path 
from lolpop.utils import common_utils as utils 
import json 
class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls = NaturalOrderGroup, help="Utilities for building deployments.")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))



@app.command("package", help="package a workflow.")
def package(
    lolpop_class: str = typer.Argument(..., help="Lolpop class to package."),
    config_file: Path = typer.Option(..., "-c", "--config-file",
                                     help="Location of runner configuration file."),
    lolpop_entrypoint: str = typer.Option("build_all", "-e", "--build-method",
                                          help="The method in the runner class to execute."),
    lolpop_module: str = typer.Option(
        "lolpop.runner", "-m", "--module", help="The lolpop module that the lolpop class belongs in."),
    flow_name: str = typer.Option(
        "prefect_entrypoint", "-f", help="The flow name to use in the entrypoint file."),
    packager_class: str = typer.Option(
        None, "--packager", help="The orchestrator class to use to package the workflow."),
    packager_args: List[str] = typer.Option(
        [], help="List of args to pass into the orchestrator class."),
    packager_kwargs: str = typer.Option(
        "{}", help="Dict (as a string) of kwargs to pass into the orchestrator class"),
    package_method: str = typer.Option("package", "-p", help="Package method"),
    package_type: str = typer.Option(
        "docker", "-t", help="Type of package resource to create."),
    packaging_args: List[str] = typer.Option(
        [], help="Arguments to pass into the package_method"),
    packaging_kwargs: str = typer.Option(
        "{}", help="Dict (as a string) of keyword arguments to pass into the package method"),
    local_file: Path = typer.Option(
        None, "-l", "--local-file", help="Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. "),
    skip_validation: bool = typer.Option(
        False, "--skip-validation", help="Skip configuration validation.")
):

    if packager_class is None:
        typer.secho("Packager class is None. Currently lolpo only supports packaging via an orchestrator. Please provide a valid orchestrator calss via '-p <orchestrator_class>'", fg="red")
        raise typer.Exit(code=1)

    plugin_mods = []
    if local_file is not None:
        cl = utils.load_module_from_file(local_file)
        plugin_mods = [cl.__name__]
    typer.secho("Loading class %s" % packager_class, fg="blue")
    packager_cl = utils.load_class(
        packager_class, plugin_mods=plugin_mods, class_type="component")
    if packager_cl is None:
        typer.secho("Failed to properly load class %s. Exiting..." %
                    packager_class, fg="red")
        raise typer.Exit(code=1)
    typer.secho("Loaded %s!" % packager_class, fg="green")

    typer.secho("Initializing class %s with config file %s" %
                (packager_class, config_file), fg="blue")
    packager = packager_cl(conf=config_file, 
                           is_standalone=True,
                           skip_config_validation=skip_validation,
                           *packager_args, **json.loads(packager_kwargs))
    typer.secho("Initialized!", fg="green")

    if hasattr(packager, package_method):
        typer.secho("Executing %s.%s with args %s and kwargs %s" % (
            packager_class, package_method, packaging_args, packaging_kwargs), fg="blue")
        func = getattr(packager, package_method)
        func(lolpop_class=lolpop_class, lolpop_module=lolpop_module, lolpop_entrypoint=lolpop_entrypoint, package_type=package_type,
             *packaging_args, **json.loads(packaging_kwargs))
        typer.secho("Packaging completed!", fg="green")
    else:
        typer.secho("ERROR: Method %s not found in class %s!" %
                    (package_method, packager_class), fg="red")



@app.command("build", help="build a deployment.")
def build(
    deployer_class: str = typer.Option(..., "--deployer", help="The orchestrator class to use to deploy the workflow."),
    config_file: Path = typer.Option(..., "-c", "--config-file",help="Location of runner configuration file."),
    deployer_args: List[str] = typer.Option([], help="List of args to pass into the orchestrator class."),
    deployer_kwargs: str = typer.Option("{}", help="Dict (as a string) of kwargs to pass into the orchestrator class"),
    deployment_method: str = typer.Option("deploy", "-d", help="Deployment method"), 
    deployment_name: str = typer.Option("lolpop-deployment", "-n", help="Name of the deployment."),
    deployment_type: str = typer.Option("docker", "-t", help="Type of deployment to create."),
    deployment_args: List[str] = typer.Option([], help="Arguments to pass into the deployment_method"), 
    deployment_kwargs: str = typer.Option("{}", help="Dict (as a string) of keyword arguments to pass into the deployment method"), 
    local_file: Path = typer.Option(
        None, "-l", "--local-file", help="Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. "),
    skip_validation: bool = typer.Option(False, "--skip-validation", help="Skip configuration validation.")
): 
    
    if deployer_class is None: 
        typer.secho("Deployer class is None. Currently lolpo only supports deployment via an orchestrator. Please provide a valid orchestrator calss via '-d <orchestrator_class>'", fg="red")
        raise typer.Exit(code=1)

    plugin_mods = []
    if local_file is not None: 
        cl = utils.load_module_from_file(local_file)
        plugin_mods = [cl.__name__]
    typer.secho("Loading class %s" %deployer_class, fg="blue")
    deployer_cl = utils.load_class(
        deployer_class, plugin_mods=plugin_mods, class_type="component")
    if deployer_cl is None:
        typer.secho("Failed to properly load class %s. Exiting..." %deployer_class, fg="red")
        raise typer.Exit(code=1)
    typer.secho("Loaded %s!" % deployer_class, fg="green")

    typer.secho("Initializing class %s with config file %s" %(deployer_class, config_file), fg="blue")
    deployer = deployer_cl(conf=config_file, 
                           is_standalone=True,
                           skip_config_validation=skip_validation,
                           *deployer_args, **json.loads(deployer_kwargs))
    typer.secho("Initialized!", fg="green")
    
    if hasattr(deployer, deployment_method):
        typer.secho("Executing %s.%s with args %s and kwargs %s" % (
            deployer_class, deployment_method, deployment_args, deployment_kwargs), fg="blue")
        func = getattr(deployer, deployment_method)
        func(deployment_name=deployment_name, deployment_type=deployment_type, 
             *deployment_args, **json.loads(deployment_kwargs))
        typer.secho("Deployment completed!", fg="green")        
    else: 
        typer.secho("ERROR: Method %s not found in class %s!" %(deployment_method, deployer_class), fg="red")


@app.command("run", help="run a deployment.")
def run(
    deployment_name: str = typer.Argument(..., help="Name of the deployment."),
    deployer_class: str = typer.Option(..., "--deployer",
                                       help="The orchestrator class to use to deploy the workflow."),
    config_file: Path = typer.Option(..., "-c", "--config-file",
                                     help="Location of runner configuration file."),
    deployer_args: List[str] = typer.Option(
        [], help="List of args to pass into the orchestrator class."),
    deployer_kwargs: str = typer.Option(
        "{}", help="Dict (as a string) of kwargs to pass into the orchestrator class"),
    run_method: str = typer.Option(
        "run", "-r", help="Run method"),
    run_args: List[str] = typer.Option(
        [], help="Arguments to pass into the deployment_method"),
    run_kwargs: str = typer.Option(
        "{}", help="Dict (as a string) of keyword arguments to pass into the deployment method"),
    local_file: Path = typer.Option(
        None, "-l", "--local-file", help="Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. "),
    skip_validation: bool = typer.Option(
        False, "--skip-validation", help="Skip configuration validation.")
):

    if deployer_class is None:
        typer.secho("Deployer class is None. Currently lolpo only supports deployment via an orchestrator. Please provide a valid orchestrator calss via '-d <orchestrator_class>'", fg="red")
        raise typer.Exit(code=1)

    plugin_mods = []
    if local_file is not None:
        cl = utils.load_module_from_file(local_file)
        plugin_mods = [cl.__name__]
    typer.secho("Loading class %s" % deployer_class, fg="blue")
    deployer_cl = utils.load_class(
        deployer_class, plugin_mods=plugin_mods, class_type="component")
    if deployer_cl is None:
        typer.secho("Failed to properly load class %s. Exiting..." %
                    deployer_class, fg="red")
        raise typer.Exit(code=1)
    typer.secho("Loaded %s!" % deployer_class, fg="green")

    typer.secho("Initializing class %s with config file %s" %
                (deployer_class, config_file), fg="blue")
    deployer = deployer_cl(conf=config_file, 
                           is_standalone=True, 
                           skip_config_validation=skip_validation,
                           *deployer_args, **json.loads(deployer_kwargs))
    typer.secho("Initialized!", fg="green")

    if hasattr(deployer, run_method):
        typer.secho("Executing %s.%s with args %s and kwargs %s" % (
            deployer_class, run_method, run_args, run_kwargs), fg="blue")
        func = getattr(deployer, run_method)
        run_id, url = func(deployment_name=deployment_name, *run_args, **json.loads(run_kwargs))
        typer.secho("Deployment ran! Created run %s. Visit %s for more information" %(run_id,url), fg="green")
    else:
        typer.secho("ERROR: Method %s not found in class %s!" %
                    (run_method, deployer_class), fg="red")


@app.command("stop", help="stop a deployment.")
def stop(
    deployer_class: str = typer.Option(..., "--deployer",
                                       help="The orchestrator class to use to deploy the workflow."),
    config_file: Path = typer.Option(..., "-c", "--config-file",
                                     help="Location of runner configuration file."),
    deployer_args: List[str] = typer.Option(
        [], help="List of args to pass into the orchestrator class."),
    deployer_kwargs: str = typer.Option(
        "{}", help="Dict (as a string) of kwargs to pass into the orchestrator class"),
    stop_method: str = typer.Option(
        "stop", "-s", help="Stop method"),
    deployment_name: str = typer.Option(
        "lolpop-deployment", "-n", help="Name of the deployment."),
    deployment_type: str = typer.Option(
        "docker", "-t", help="Type of deployment to create."),
    stop_args: List[str] = typer.Option(
        [], help="Arguments to pass into the deployment_method"),
    stop_kwargs: str = typer.Option(
        {}, help="Dict (as a string) of keyword arguments to pass into the deployment method"),
    local_file: Path = typer.Option(
        None, "-l", "--local-file", help="Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. "),
    skip_validation: bool = typer.Option(
        False, "--skip-validation", help="Skip configuration validation.")
):

    if deployer_class is None:
        typer.secho("Deployer class is None. Currently lolpo only supports deployment via an orchestrator. Please provide a valid orchestrator calss via '-d <orchestrator_class>'", fg="red")
        raise typer.Exit(code=1)

    plugin_mods = []
    if local_file is not None:
        cl = utils.load_module_from_file(local_file)
        plugin_mods = [cl.__name__]
    typer.secho("Loading class %s" % deployer_class, fg="blue")
    deployer_cl = utils.load_class(
        deployer_class, plugin_mods=plugin_mods, class_type="component")
    if deployer_cl is None:
        typer.secho("Failed to properly load class %s. Exiting..." %
                    deployer_class, fg="red")
        raise typer.Exit(code=1)
    typer.secho("Loaded %s!" % deployer_class, fg="green")

    typer.secho("Initializing class %s with config file %s" %
                (deployer_class, config_file), fg="blue")
    deployer = deployer_cl(conf=config_file, 
                           is_standalone=True, 
                           skip_config_validation=skip_validation,
                           *deployer_args, **json.loads(deployer_kwargs))
    typer.secho("Initialized!", fg="green")

    if hasattr(deployer, stop_method):
        typer.secho("Executing %s.%s with args %s and kwargs %s" % (
            deployer_class, stop_method, stop_args, stop_kwargs), fg="blue")
        func = getattr(deployer, stop_method)
        func(deployment_name=deployment_name, deployment_type=deployment_type,
             *stop_args, **json.loads(stop_kwargs))
        typer.secho("Finished stop!", fg="green")
    else:
        typer.secho("ERROR: Method %s not found in class %s!" %
                    (stop_method, deployer_class), fg="red")
