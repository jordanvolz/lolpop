
It's relatively easy to get started with extensions in lolpop. By using the lolpop cli and taking advantage of pre-built templates, you can quickly bootstrap new extension building. 


## Creating a Project

It's highly recommended to take advantage of lolpop's built-in [projects](lolpop_projects.md) when creating an extension. This will do some light organizing for you which will make packaging the project up later much easier. To create a lolpop project, simply execute the following command: 

```bash
lolpop init project_name --project_path /path/to/project
```

This will create a new project structure at the path `/path/to/project/project_name`. In that directory, the `lolpop` subdirectory is what you'll want to use to build all extensions for your project. 

## Creating Extensions via Templates 

lolpop has built-in templates for all integration types. If you're working on your first extension, it is highly recommend to leverage these templates. 

### Creating a Component / Pipeline / Runner

To create a new integration from the lolpop template, simply execute the following command: 

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

In the above example, `extension_name` is the name of the extension you are creating, `<integration_type>` is the generic type of integration, such as `metadata_tracker`, and `<integration_class>` is the specific class you wish to create, such as `mlflow_metadata_tracker`.

!!! Note 
    Both `<integration>_class` and `<integration>_type` should be [snake case](https://en.wikipedia.org/wiki/Snake_case).  
!!! Note
    It's possible to group several new integrations under the same `extension_name`.

lolpop will then create the templated integration under `</path/to/project/project_name>/lolpop/extension/<extension_name>/<integration>/<integration_type>/`. In this directory will be two files: `base_<integration_type>.py` and `<integration_class>.py`. These are the files you'll want to customize to build your extension!

Note that if you try to create more than one `integration_class` under the same `integration_type`, lolpop will return an error telling you the directory already exists for anything more than the first integration. This is due to the underlying libraries lolpop uses to create and copy templates. If you have a need to to have multiple classes under the same type, simply cut and paste as many templated classes as you need. 

## Using Your Own Extensions Templates

As you gain familiarity with lolpop you may wish to develop more customized templates to your own organizations coding or development styles. lolpop can take custom template paths as an additional option via `--template-path`. This can either be a local directory or a git url. 

lolpop uses `cookiecutter` to build templates, so your custom templates also need to be compliant with cookiecutter syntax. 

If you wish to forge your own path completely with templates, it's recommended to look into [extending lolpop's cli](extending_cli.md).