
## Executing Workflows 

=== "Python"
    ```python 
    from lolpop.extensions import MyRunner

    config_file = "/path/to/dev.yaml"

    runner = MyRunner(conf=config_file)

    ...

    model = runner.train.train_model(data)

    ... 
    ``` 

=== "CLI"
    ```bash
    lolpop run workflow MyRunner --config-file /path/to/dev.yaml
    ```

## Environments


## CI/CD considerations