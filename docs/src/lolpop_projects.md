
The lolpop cli contains a command for creating lolpop projects. A lolpop project is a great place to begin designing your own workflows, especially if you intend to write your own extensions. Even if you don't plan to write your own extensions, you may find benefits from organizing your projects in a standardized way. 

Today, lolpop doesn't currently take advantage of users leveraging lolpop projects, but we envision this will be the case in the future.

## Creating a lolpop project 

lolpop projects can easily be created via the command line: 

```bash 

lolpop init project_name --project_path /path/to/project
```

In the above, we're creating a new project `project_name` in the directory `/path/to/project`. When you install lolpop, you also install many default templates that lolpop will use for project creation and more, but if you wish to use a different project setup, you can override the template source via the argument `--template-path`. This can either be a local directory or a git url. 


## Project Structure

The lolpop project structure is currently as follows: 

```bash 
/project_name
|-- /config
|-- /data 
|-- /docs
|-- /lolpop
|-- /models
|-- /notebooks
|-- /scripts
|-- /tests
|-- lolpop_project.yaml
|-- Makefile
|-- pyproject.toml
|-- README.md
```

And here's a quick description of what we envision each to be used for: 

- `config/`: Stores various lolpop configuration files for use. 

- `data/`: Stores data for your project locally. Note, we'd typically recommend using a proper data store and a `data_connector` in your workflow, but sometimes you just need to store something locally. If so, a good practice is to leverage `lolpop seed` when needed and also to version via your `resource_version_control` component. 

- `docs/`: Documentation for whatever you are building. 

- `lolpop/`: This will contain all extensions you build. You should start all extensions via the `lopop create` command. 

- `models/`: Similarly to `data/`, this is a directory where you can locally store models created with lolpop, but we'd recommend using a proper `model_repository`. 

- `notebooks/`: In case you have a need to use notebooks, you can store them here. 

- `scripts/`: This should contain your small scripts initiating runner workflows via files in `config/`. 

- `tests/`: This should contain unit tests of any extensions you're building as well as workflow tests using lolpop's testing framework. 

- `lolpop_project.yaml`: The lolpop project file! Unused for now, but we have great things planned. 

- `Makefile`: a place to built shortcuts for common development or deployment tasks. Empty for now but we'll likely include some common tasks in the future. 

- `pyproject.toml`: If you're building extensions, this is the place to define dependencies and also control the packaging behavior of your extension. 

- `README.md`: A place to let people know what you're working on. 