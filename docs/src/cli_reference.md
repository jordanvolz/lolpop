# `lolpop`

lolpop: A software engineering framework for machine learning workflows.

**Usage**:

```console
$ lolpop [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Print lolpop version
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `init`: Initialize a lolpop project.
* `help`: Show CLI usage help.
* `list-extras`: list available extra packages
* `run`: Run workflows with lolpop.
* `create`: Create new runners, pipelines, and...
* `datagen`: Generate synthetic data from existing data.
* `seed`: Upload local data into your data platform.
* `test`: Test lolpop runners, pipelines, and...
* `deployment`: Utilities for building deployments.
* `extension`: Run lolpop CLI extensions.

## `lolpop init`

Initialize a lolpop project.

**Usage**:

```console
$ lolpop init [OPTIONS] PROJECT_NAME
```

**Arguments**:

* `PROJECT_NAME`: Name of the project to create.  [required]

**Options**:

* `--project-path PATH`: Path to create project.  [default: /Users/jordanvolz/github/lolpop]
* `--template-path TEXT`: Path to the project template.  [default: /Users/jordanvolz/github/lolpop/lolpop/templates/project_template]
* `--help`: Show this message and exit.

## `lolpop help`

Show CLI usage help.

## `lolpop list-extras`

list available extra packages

**Usage**:

```console
$ lolpop list-extras [OPTIONS]
```

**Options**:

* `--package-name TEXT`: Name of package to list available extras for.  [default: lolpop]
* `--print-reqs`: Print depencencies included in the extra packages.
* `--help`: Show this message and exit.

## `lolpop run`

Run workflows with lolpop.

**Usage**:

```console
$ lolpop run [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `workflow`: Run a workflow.

### `lolpop run workflow`

Run a workflow.

**Usage**:

```console
$ lolpop run workflow [OPTIONS] RUNNER_CLASS
```

**Arguments**:

* `RUNNER_CLASS`: Runner class.  [required]

**Options**:

* `-c, --config-file PATH`: Location of runner configuration file.  [required]
* `-b, --build-method TEXT`: The method in the runner class to execute.  [default: main]
* `--build-args TEXT`: List of args to pass into build_method.
* `--build-kwargs TEXT`: Dict (as a string) of kwargs to pass into build_method  [default: {}]
* `-l, --local-file PATH`: Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. 
* `--skip-validation`: Skip configuration validation.
* `--help`: Show this message and exit.

## `lolpop create`

Create new runners, pipelines, and components.

**Usage**:

```console
$ lolpop create [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `component`: Initialize a custom component.
* `pipeline`: Initialize a custom pipeline.
* `runner`: Initialize a custom runner.
* `cli-command`: Initialize a custom cli command.
* `documentation`: Create documentation for a class.
* `tests`: Create tests for a class.
* `docstrings`: Create docstrings for a class.

### `lolpop create component`

Initialize a custom component.

**Usage**:

```console
$ lolpop create component [OPTIONS] COMPONENT_TYPE COMPONENT_CLASS EXTENSION_NAME
```

**Arguments**:

* `COMPONENT_TYPE`: Component type (Should be snake_case).  [required]
* `COMPONENT_CLASS`: Component class name (Should be snake_case).  [required]
* `EXTENSION_NAME`: Name of the parent extension for this resource.  [required]

**Options**:

* `--template-path TEXT`: Path to the template file. Or a git url of a template file.  [default: /Users/jordanvolz/github/lolpop/lolpop/templates/component_template]
* `--project-dir PATH`: Project directory for the new component.  [default: /Users/jordanvolz/github/lolpop]
* `--help`: Show this message and exit.

### `lolpop create pipeline`

Initialize a custom pipeline.

**Usage**:

```console
$ lolpop create pipeline [OPTIONS] PIPELINE_TYPE PIPELINE_CLASS EXTENSION_NAME
```

**Arguments**:

* `PIPELINE_TYPE`: Pipeline type (Should be snake_case).  [required]
* `PIPELINE_CLASS`: Pipeline class name (Should be snake_case).  [required]
* `EXTENSION_NAME`: Name of the parent extension for this resource.  [required]

**Options**:

* `--template-path TEXT`: Path to the template file. Or a git url of a template file.  [default: /Users/jordanvolz/github/lolpop/lolpop/templates/pipeline_template]
* `--project-dir PATH`: Parent directory for the new pipeline.  [default: /Users/jordanvolz/github/lolpop]
* `--help`: Show this message and exit.

### `lolpop create runner`

Initialize a custom runner.

**Usage**:

```console
$ lolpop create runner [OPTIONS] RUNNER_TYPE RUNNER_CLASS EXTENSION_NAME
```

**Arguments**:

* `RUNNER_TYPE`: Component type (Should be snake_case)  [required]
* `RUNNER_CLASS`: Component class name (Should be snake_case).  [required]
* `EXTENSION_NAME`: Name of the parent extension for this resource.  [required]

**Options**:

* `--template-path TEXT`: Path to the template file. Or a git url of a template file.  [default: /Users/jordanvolz/github/lolpop/lolpop/templates/runner_template]
* `--project-dir PATH`: Parent directory for the new component.  [default: /Users/jordanvolz/github/lolpop]
* `--help`: Show this message and exit.

### `lolpop create cli-command`

Initialize a custom cli command.

**Usage**:

```console
$ lolpop create cli-command [OPTIONS] COMMAND_NAME
```

**Arguments**:

* `COMMAND_NAME`: Name of the cli command to create. (Use Snake Case)  [required]

**Options**:

* `--template-path TEXT`: Path to the template file. Or a git url of a template file.  [default: /Users/jordanvolz/github/lolpop/lolpop/templates/cli_template]
* `--command-description TEXT`: description for the command_name
* `--project-dir PATH`: Parent directory for the new component.  [default: /Users/jordanvolz/github/lolpop]
* `--help`: Show this message and exit.

### `lolpop create documentation`

Create documentation for a class.

**Usage**:

```console
$ lolpop create documentation [OPTIONS] SOURCE_FILE CLASS_NAME
```

**Arguments**:

* `SOURCE_FILE`: Path to the source file.  [required]
* `CLASS_NAME`: Class name in source_file to document.  [required]

**Options**:

* `-f, --method-filter TEXT`: Methods to include in the documentation. default=all.
* `-g, --generator-class TEXT`: Generative AI Chatbot class name.  [default: OpenAIChatbot]
* `-k, --kwargs TEXT`: Keyword arguments to pass into the generator class  [default: {}]
* `-o, --output-path PATH`: The location to save the documentation
* `-d, --documentation-format TEXT`: The format you would like the documentation to be written in.  [default: markdown]
* `--help`: Show this message and exit.

### `lolpop create tests`

Create tests for a class.

**Usage**:

```console
$ lolpop create tests [OPTIONS] SOURCE_FILE CLASS_NAME
```

**Arguments**:

* `SOURCE_FILE`: Path to the source file.  [required]
* `CLASS_NAME`: Class name in source_file to document.  [required]

**Options**:

* `-f, --method-filter TEXT`: Methods to include in the documentation. default=all.
* `-g, --generator-class TEXT`: Generative AI Chatbot class name.  [default: OpenAIChatbot]
* `-k, --kwargs TEXT`: Keyword arguments to pass into the generator class  [default: {}]
* `-o, --output-path PATH`: The location to save the documentation
* `-t, --testing-framework TEXT`: The testing framework you would like the tests to be written in.  [default: pytest]
* `--help`: Show this message and exit.

### `lolpop create docstrings`

Create docstrings for a class.

**Usage**:

```console
$ lolpop create docstrings [OPTIONS] SOURCE_FILE CLASS_NAME
```

**Arguments**:

* `SOURCE_FILE`: Path to the source file.  [required]
* `CLASS_NAME`: Class name in source_file to document.  [required]

**Options**:

* `-f, --method-filter TEXT`: Methods to include in the documentation. default=all.
* `-g, --generator-class TEXT`: Generative AI Chatbot class name.  [default: OpenAIChatbot]
* `-k, --kwargs TEXT`: Keyword arguments to pass into the generator class  [default: {}]
* `-o, --output-path PATH`: The location to save the documentation
* `-d, --docstring-format TEXT`: The format you would like the docstring to be written in.  [default: Google]
* `--help`: Show this message and exit.

## `lolpop datagen`

Generate synthetic data from existing data.

**Usage**:

```console
$ lolpop datagen [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a synthetic dataset.

### `lolpop datagen create`

Create a synthetic dataset.

**Usage**:

```console
$ lolpop datagen create [OPTIONS] SOURCE_FILE
```

**Arguments**:

* `SOURCE_FILE`: Path to the source file.  [required]

**Options**:

* `-c, --datagen-class TEXT`: Data Synthesizer class name.  [default: SDVDataSynthesizer]
* `-s, --synthesizer-class TEXT`: Class name in the data synthesizer to use to build a synthesizer model.  [default: SingleTablePreset]
* `-n, --num-rows INTEGER`: The number of rows to generate for the synthetic data.  [default: 10000]
* `-o, --output-path PATH`: The location to save the generated_data  [default: /Users/jordanvolz/github/lolpop]
* `--evaluate-fake-data`: Run evaluator on fake data.
* `--help`: Show this message and exit.

## `lolpop seed`

Upload local data into your data platform. 

**Usage**:

```console
$ lolpop seed [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `file`: Seed a file.

### `lolpop seed file`

Seed a file.

**Usage**:

```console
$ lolpop seed file [OPTIONS] SOURCE_FILE TARGET
```

**Arguments**:

* `SOURCE_FILE`: Path to the source file  [required]
* `TARGET`: Where the data is going. Should be a table in DW or path in the object store, etc.  [required]

**Options**:

* `-c, --data-connector-class TEXT`: Data Connector class name.
* `-k, --kwargs TEXT`: Keyword arguments (as a string) to pass into the data connector.  [default: {}]
* `--help`: Show this message and exit.

## `lolpop test`

Test lolpop runners, pipelines, and components.

**Usage**:

```console
$ lolpop test [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `workflow`: Test a workflow.

### `lolpop test workflow`

Test a workflow.

**Usage**:

```console
$ lolpop test workflow [OPTIONS] INTEGRATION_CLASS TEST_CONFIG
```

**Arguments**:

* `INTEGRATION_CLASS`: Integration class to test.  [required]
* `TEST_CONFIG`: Location of the testing configuration file.  [required]

**Options**:

* `--integration-config PATH`: Location of integration configuration file. Optional. If not provided, lolpop will attempt to use the testing configurationa as the runner configuration as well.
* `--integration-type TEXT`: The type of class to test: runner, pipeline, componenet, etc.  [default: runner]
* `--build-method TEXT`: The method in the integration class to execute.  [default: main]
* `--build-args TEXT`: List of args to pass into build_method.
* `--build-kwargs TEXT`: Dict (as a string) of kwargs to pass into build_method  [default: {}]
* `--help`: Show this message and exit.

## `lolpop deployment`

Utilities for building deployments.

**Usage**:

```console
$ lolpop deployment [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `package`: package a workflow.
* `build`: build a deployment.
* `run`: run a deployment.
* `stop`: stop a deployment.

### `lolpop deployment package`

package a workflow.

**Usage**:

```console
$ lolpop deployment package [OPTIONS] LOLPOP_CLASS
```

**Arguments**:

* `LOLPOP_CLASS`: Lolpop class to package.  [required]

**Options**:

* `-c, --config-file PATH`: Location of runner configuration file.  [required]
* `-e, --build-method TEXT`: The method in the runner class to execute.  [default: build_all]
* `-m, --module TEXT`: The lolpop module that the lolpop class belongs in.  [default: lolpop.runner]
* `-f TEXT`: The flow name to use in the entrypoint file.  [default: prefect_entrypoint]
* `--packager TEXT`: The orchestrator class to use to package the workflow.
* `--packager-args TEXT`: List of args to pass into the orchestrator class.
* `--packager-kwargs TEXT`: Dict (as a string) of kwargs to pass into the orchestrator class  [default: {}]
* `-p TEXT`: Package method  [default: package]
* `-t TEXT`: Type of package resource to create.  [default: docker]
* `--packaging-args TEXT`: Arguments to pass into the package_method
* `--packaging-kwargs TEXT`: Dict (as a string) of keyword arguments to pass into the package method  [default: {}]
* `-l, --local-file PATH`: Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. 
* `--skip-validation`: Skip configuration validation.
* `--help`: Show this message and exit.

### `lolpop deployment build`

build a deployment.

**Usage**:

```console
$ lolpop deployment build [OPTIONS]
```

**Options**:

* `--deployer TEXT`: The orchestrator class to use to deploy the workflow.  [required]
* `-c, --config-file PATH`: Location of runner configuration file.  [required]
* `--deployer-args TEXT`: List of args to pass into the orchestrator class.
* `--deployer-kwargs TEXT`: Dict (as a string) of kwargs to pass into the orchestrator class  [default: {}]
* `-d TEXT`: Deployment method  [default: deploy]
* `-n TEXT`: Name of the deployment.  [default: lolpop-deployment]
* `-t TEXT`: Type of deployment to create.  [default: docker]
* `--deployment-args TEXT`: Arguments to pass into the deployment_method
* `--deployment-kwargs TEXT`: Dict (as a string) of keyword arguments to pass into the deployment method  [default: {}]
* `-l, --local-file PATH`: Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. 
* `--skip-validation`: Skip configuration validation.
* `--help`: Show this message and exit.

### `lolpop deployment run`

run a deployment.

**Usage**:

```console
$ lolpop deployment run [OPTIONS] DEPLOYMENT_NAME
```

**Arguments**:

* `DEPLOYMENT_NAME`: Name of the deployment.  [required]

**Options**:

* `--deployer TEXT`: The orchestrator class to use to deploy the workflow.  [required]
* `-c, --config-file PATH`: Location of runner configuration file.  [required]
* `--deployer-args TEXT`: List of args to pass into the orchestrator class.
* `--deployer-kwargs TEXT`: Dict (as a string) of kwargs to pass into the orchestrator class  [default: {}]
* `-r TEXT`: Run method  [default: run]
* `--run-args TEXT`: Arguments to pass into the deployment_method
* `--run-kwargs TEXT`: Dict (as a string) of keyword arguments to pass into the deployment method  [default: {}]
* `-l, --local-file PATH`: Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. 
* `--skip-validation`: Skip configuration validation.
* `--help`: Show this message and exit.

### `lolpop deployment stop`

stop a deployment.

**Usage**:

```console
$ lolpop deployment stop [OPTIONS]
```

**Options**:

* `--deployer TEXT`: The orchestrator class to use to deploy the workflow.  [required]
* `-c, --config-file PATH`: Location of runner configuration file.  [required]
* `--deployer-args TEXT`: List of args to pass into the orchestrator class.
* `--deployer-kwargs TEXT`: Dict (as a string) of kwargs to pass into the orchestrator class  [default: {}]
* `-s TEXT`: Stop method  [default: stop]
* `-n TEXT`: Name of the deployment.  [default: lolpop-deployment]
* `-t TEXT`: Type of deployment to create.  [default: docker]
* `--stop-args TEXT`: Arguments to pass into the deployment_method
* `--stop-kwargs TEXT`: Dict (as a string) of keyword arguments to pass into the deployment method  [default: {}]
* `-l, --local-file PATH`: Local file to use to read class definition instead of reading directly from lolpop. Useful when you want to run a modified local class that isn't properly registered. 
* `--skip-validation`: Skip configuration validation.
* `--help`: Show this message and exit.

## `lolpop extension`

Run lolpop CLI extensions.

**Usage**:

```console
$ lolpop extension [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.
