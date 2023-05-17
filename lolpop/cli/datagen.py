import typer 
from lolpop.utils import common_utils as utils
from pathlib import Path
import os 
from typer.core import TyperGroup


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx):
        return self.commands.keys()
    
app = typer.Typer(cls = NaturalOrderGroup, help="Generate synthetic data from existing data.")


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        typer.echo(ctx.command.get_help(ctx))

@app.command("create", help="Create a synthetic dataset.")
def create(
    source_file: Path = typer.Argument(
        ..., help="Path to the source file."),
    datagen_class: str = typer.Option("SDVDataSynthesizer", "--datagen-class", "-c", help="Data Synthesizer class name."),
    synthesizer_class: str = typer.Option(
        "SingleTablePreset", "--synthesizer-class", "-s", help="Class name in the data synthesizer to use to build a synthesizer model."),

    num_rows: int = typer.Option(10000, "--num-rows", "-n", help="The number of rows to generate for the synthetic data."),
    output_path: Path = typer.Option(os.getcwd(), "--output-path", "-o", help="The location to save the generated_data"),
    evaluate_fake_data: bool = typer.Option(False, "--evaluate-fake-data", help="Run evaluator on fake data.")
): 
    typer.secho("Loading datagen class %s" %datagen_class, fg="blue")
    datagen_cl = utils.load_class(datagen_class, "component")
    logger_cl = utils.load_class("StdOutLogger", "component")
    data_generator = datagen_cl(components={"logger": logger_cl()})
    data_generator.suppress_logger = True 
    data_generator.suppress_notifier = True 
    typer.secho("Successfully loaded datagen class %s" % datagen_class, fg="green")

    typer.secho("Loading data for synthesizer from %s" % source_file, fg="blue")
    data, metadata = data_generator.load_data(str(source_file))
    typer.secho("Successfully loaded data!", fg="green")

    typer.secho("Building data synthesizer model. This can take awhile ...", fg="blue")
    synthesizer = data_generator.model_data(data, metadata, synthesizer_class)
    typer.secho("Successfully built data synthesizer model!", fg="green")

    typer.secho("Creating synthetic dataset with %s rows" % num_rows, fg="blue")
    fake_data = data_generator.sample_data(synthesizer, num_rows)
    typer.secho("Successfully created synthetic data! Here's a preview of the first 5 rows:", fg="green")
    typer.secho(fake_data.head())

    if evaluate_fake_data: 
        typer.secho("Evaluating synthetic dataset...", fg="blue")
        quality_report, diagnostic_report = data_generator.evaluate_data(data, fake_data, metadata, synthesizer_class)
        typer.secho("Successfully evaluated synthetic data!", fg="green")

    typer.secho("Saving synthetic data to output directory %s" % output_path, fg="blue")   
    (source_file_name, source_file_type) = str(source_file).split("/")[-1].split(".")
    output_file_path = "%s/%s_syn.%s" %(output_path, source_file_name, source_file_type)
    if source_file_type == "csv": 
        fake_data.to_csv(output_file_path, index=False)
    elif source_file_type in ["parquet", "pq"]: 
        fake_data.to_parquet(output_file_path, index=False)
    else: 
        typer.secho("Unsupported file type: %s" %source_file_type, fg="red")
    typer.secho("Successfully saved synthetic data to %s!" %output_file_path, fg="green")
    
