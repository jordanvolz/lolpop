
Many of lolpop's [CLI](cli.md) commands are inspired from integrations that we build. After building a cool integration, it's often a easy to see how exposing part of it as a CLI command would generate a lot of value for users. We expect people may feel the same as they begin building extension and so, the CLI itself is also extensible. When we say this we mean two main things: 

1. When we build command we try to do so in a way that is pluggable. That is, users can use the same command put swap out the integration or extension class used without having to rewrite any code. For example, the default generative AI integration for automating test creation, docstrings, and documentation uses ChatGPT, but it can easily be swapped out for a different chatbot experience, like Gooble Bard or Github Copilot. 

2. When users are building new extensions they can also build a new lolpop CLI command. Once your package is installed on a system with lolpop, lolpop will then be able to expose that command as part of the normal CLI experience. 

Sounds cool, right? Let's see how it works. 

## Creating CLI Extension via Template 

As with most things extension-related, we highly recommend getting started with a [lolpop project](lolpop_projects.md). If you're doing that, then you can quickly define a new CLI extension via the following command. 

```bash 
lolpop create cli-command <command_name> --project-dir /path/to/project
```

In the above example, `command_name` is the name of the command that you wish to register with lolpop. This should be snake case. lolpop will then generate a template file in your project path `/path/to/project/lolpop/cli/extensions/<command_name>/`. This directory will have a file `<command_name>.py` that will contain a templated file to create a CLI command. 

Lolpop utilizes [Typer](https://typer.tiangolo.com/) for its CLI framework, so some knowledge of how to create typer commands will be useful, but here's a quick MVP for those who are new. 

In your `<command_name>.py` file, you'll create a new method for every command you'll want to expose via this CLI extension. Your templated command will look like this: 

```python
@app.command("my-first-command", help="This is the first command in the command group.")
def my_first_command(
    my_first_argument: str = typer.Argument(..., help="A description of this argument"),
    my_first_option: str = typer.Option(None, help="A description of this option."),
    my_second_option: str = typer.Option(None, help="A description of this option."),
): 
    #your code here 
    pass 
```

You'll want to change the following: 

1. In `@app.command` change the command name (i.e. `my-first-command`) and the help text. This is the name of the command you'll be exposing in the CLI. Note that the method name (i.e. `my_first_command`) isn't actually used for anything but it's best practice to map it closely to the actual command name. Note that these commands here are actually subcommands from the main `<command_name>.py`. You can include many commands/methods here via `@app.command` and each will be nested under `<command_name>` in the CLI. 

2. Update all the arguments to your command to represent the inputs you want people to be able to pass in, add default values, if applicable, and update the help text. Typer has two main inputs to a command: `arguments` are passed in directly after the command and `options` are passed in via a flag (either `-o` or `--option` for example). Use `typer.Argument` and `typer.Option` to specify how uses should specify information and the first argument of each is the default value. Note here that `...` specifies a required value (i.e. no default is used). 

3. Implement your command! Write the code you want to accomplish the task you seek to expose to users. 

## Using Your CLI Extension

Once you're finished creating a CLI extension, you'll want to [package and install](packaging_extensions.md) it like any other extension. This will register the extension with lolpop, and you'll then be able to use the extension via the following command: 

```bash
lolpop extension <command_name> <sub_command_name> <arguments> <options> 
```
So, for example, let's pretend we created the following under `my_new_command.py`: 

```python
@app.command("my-first-command", help="This is the first command in the command group.")
def my_first_command(
    my_first_argument: str = typer.Argument(..., help="A description of this argument"),
    my_first_option: str = typer.Option(None, "-o", help="A description of this option."),
): 
    print("My first argument: %s" %my_first_argument)
    print("My first option: %s" %my_first_option)
```

Once we install the extension we can then invoke this via the command: 

```bash
lolpop extension my-new-command my-first-command "Hello World!" -o "Good bye!"
```

And we would get the output

```bash 
My first argument: Hello World! 
My first option: Good bye! 
```