
## Executing Workflows 

lolpop contains two main ways to execute a workflow. You can either execute a workflow directly using a runner class, or via the lolpop CLI. 

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

We would typically expect that production scripts may execute one or more workflows defined in a runner. For example, for a single use case you may need to: 

1. Pull training data and refresh the model on a given cadence (i.e. weekly, monthly, quarterly, etc.)
2. Pull prediction data and regenerate predictions on a given cadence (i.e. weekly, daily, hourly, etc.)
3. Occasionally rebuild the entire use case from scratch (i.e. pull all data, rebuild models, deploy models, generate predictions, etc.)

Your scripts can easily chain together runner workflows as needed to arrive at your desired state. 

## Environments
Although lolpop has no concept of environments, we believe that all the tools are provided to give users the desired experience. 

You certainly should be utilizing, and also testing workflows out in different environments: development, staging/test, production, etc.. The differences between environments is sometimes stark, and sometimes not. I.e. perhaps development is done locally w/ pandas & local python, and production is in a distributed Spark cluster. 

Our expectation is that the main differences between environments should be the components utilized, and not the makeup of the workflows themselves. That is, you should be able to leverage the same runner, and very likely the same pipelines, while just switching components between environments or even *only* switching configuration on the same component (for example, perhaps dev and production merely pull from different schemas in your data warehouse). 

Thus, our guidance for working with environments is that you should maintain separate configuration files for each environment. It's perfectly acceptable that a project folder might look something like: 

```bash 
customer_churn/
|-- dev.yaml 
|-- staging.yaml
|-- prod.yaml 
|-- run.py 
```

You should also be sure to version all your project file in your source repository of choice as well. 

## Working with Orchestrators
In the future we plan to build out some cooler integrations with well-known and popular orchestration tools, but for now we believe that the ability to execute lolpop workflows entirely within python or bash scripting should enable pretty straightforward integrations into your orchestrator of choice, as most of them are able to execute arbitrary python and/or bash commands. 

Feel free to get in touch if you believe there is a gap here. Likewise, if you're using lolpop with an orchestrator and would like to share your experience. We'd love to hear about it. 
## Working with CI/CD Tools
Those wishing to hook lolpop into their favorite CI/CD tool of choice should find the CLI to be their main point of integration. Again, it should be fairly straightforward to get your CI/CD tool to execute the proper lolpop workflow given a runner script, a configuration file (perhaps corresponding to a target environment?), and acess to the lopop CLI. 

Feel free to get in touch if you believe there is a gap here. Likewise, if you're using lolpop with an CI/CD tool and would like to share your experience. We'd love to hear about it. 