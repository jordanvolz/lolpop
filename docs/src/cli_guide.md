The lolpop CLI contains many built-in commands for common functionality. In this second we'll provide an overview of the commands available and how to use them. For more information on all options available, refer to the [CLI reference](cli_reference.md). You can additionally view all options for a command via the `--help` or `-h` flag when using `lolpop`: 

```bash
lolpop <command> --help
``` 

## lolpop 

lolpop contains only a couple of top-level commands. Most functionality is buried within subcommands. The two top-level commands of note are: 

- `lolpop init` 

- `lolpop list-extras`

### lolpop init 

This command bootstraps a new lolpop project. See the [lolpop project documentation](lolpop_projects.md) for more information on the structure of lolpop projects

Example: 
```bash
lolpop init my_cool_project --project-path ~/lolpop_projects/
```

### lolpop list-extras

This command lists all extra packages available to download from lolpop. See the [installation documentation](installation.md) for more information.

Example: 
```bash
lolpop list-extras
```

## lolpop run workflow

This command runs a lolpop workflow. Most often you'll wish to run part of a runner with this command. See the [documentation on running workflows](running_workflows.md#executing-workflows) for more information. 

Example: 
```bash
lolpop run workflow MyRunner --config-file dev.yaml --build-method train_model --build-kwargs "{...}"
```

## lolpop test workflow

This command tests a lolpop workflow. You'll need to provide a proper test configuration file. See the [workflow testing documentation](testing_workflows.md) for more information.  

Example: 
```bash
lolpop test workflow XGBoostTrainer xgboost_tests.yaml --build-method fit --build-kwargs "{...}"
```

## lolpop deployment 

`lolpop deployment` allows users to build, deploy, and run workflows on external systems. 

be sure to visit the [CLI reference](cli_reference.md) for all available options. 

### lolpop deployment package

In order to package a lolpop class, you'll need to provide the packaging class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for packaging via `-p` and any keyword arguments via `--packaging-kwargs`

```bash 
lolpop deployment package <lolpop_class> --packager <PackagerClass> -c /path/to/packager_config.yaml -p <package_method> --packaging_kwargs {<dict_values>}
```

Typically, the expectation is that this creates something like a docker image that can then be deployed via `lolpop deployment build`.

### lolpop deployment build 

In order to deploy a packaged workflow, you'll need to provide the Deployer class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for deployment via `-d` and any keyword arguments via `--deployment-kwargs`

```bash 
lolpop deployment build --deployer <DeployerClass> -c /path/to/deployer_config.yaml -d <deployment_method> --deployment_kwargs {<dict_values>}
```

This action should create/register a deployment with the deployer for future use. 

### lolpop deployment run 

In order to run a deployed workflow, you'll need to provide the Deployer class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for run via `-r` and any keyword arguments via `--run-kwargs`

```bash 
lolpop deployment run <deployment_name> --deployer <DeployerClass> -c /path/to/deployer_config.yaml -d <run_method> --run_kwargs {<dict_values>}
```

This should create a workflow instance in the deployer. 

### lolpop deployment stop 

In order to stop a deployed workflow, you'll need to provide the Deployer class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for run via `-s` and any keyword arguments via `--run-kwargs`

```bash 
lolpop deployment stop <deployment_name> --deployer <DeployerClass> -c /path/to/deployerclass_config.yaml -d <package_method> --stop_kwargs {<dict_values>}
```


## lolpop create 

`lolpop create` serves two main purposes: 

1. Creating skeleton extension files from a template. 

2. Using generative AI to create tests and documentation for extensions. 

### lolpop create component / pipeline/ runner / CLI Command

This command will create a new component / pipeline / runner / CLI command in your lolpop project. See the documentation on [building extenions](building_extensions.md) and [extending the cli](extending_cli.md) for more information. 

Example: 

=== "Component"
    ```bash
    lolpop create component <component_type> <component_class> <extension_name> --project_dir /path/to/project/project_name
    ```
=== "Pipeline" 
    ```bash
    lolpop create pipeline <pipeline_type> <pipeline_class> <extension_name> --project_dir /path/to/project/project_name
    ```
=== "Runner" 
    ```bash
    lolpop create runner <runner_type> <runner_class> <extension_name> --project_dir /path/to/project/project_name
    ```
=== "CLI Command" 
    ```bash
    lolpop create cli-command <command_name> --project_dir /path/to/project/project_name
    ```

### lolpop create documentation / docstrings / tests 

This command uses generative AI to build documentation, docstrings, and tests. This can help automate mundane tasks for the developer. See the documentation on  [extension documentation](writing_extension_documentation.md), and [extension tests](writing_extension_tests.md) for more information. 

Example: 

=== "Documentation" 
    ```bash 
    lolpop create documentation <source_file> <class_name> --output-path my_extension_documentation.md
    ```
=== "docstrings" 
    ```bash 
    lolpop create docstrings <source_file> <class_name> --output-path my_extension_docstrings.py
    ```
=== "Tests" 
    ```bash 
    lolpop create tests <source_file> <class_name> --output-path my_extension_tests.py
    ```

## lolpop seed file 

This command uploads a local file to a data platform using a lolpop `DataConnector` class. While this command is not meant for production work, it's sometimes useful to have an easy way to upload small and medium files on the command line while doing development work. 

Example: 
```bash 
lolpop seed file <file path> <target> --data-connector-class SnowflakeDataConnector --kwargs "{...}"
``` 

Like many of the other CLI commands, this is pluggable, so if you end up building your own data connector you can then leverage it directly in this command by referencing the class name. 

## lolpop datagen create 

This command uses synthetic data tools to generate data given a source sample. There are instances where it is nice to be able to generate a larger file from a smaller file, and synthetic data tools enable this. 

Example: 
```bash
lolpop datagen create <source_file> --datagen-class SDVDataSynthesizer -output-path /path/to/new/data.csv
```
This is also a pluggable command. Currently the `SDVDataSynthesizer` is the only synthethic data tool that is built into lolpop, but you can create your own via an extension and/or we may provide support for other synthetic data tools in the future. 

## lolpop extension

This is the entry point for any CLI extensions you have installed. See the documentation on [extending the CLI for more information](extending_cli.md).

Example: 
```bash
lolpop extension <command> <subcommand> <ags> <options>
```
