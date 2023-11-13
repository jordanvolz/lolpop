
In this section we'll cover the use of external orchestrators in lolpop. Be sure to check out the [integration documentation](base_orchestrator.md) for specific examples of built-in orchestrators. 

## Why use Orchestrators? 

Using an external orchestrator can provide many benefits to your workflow. Although lolpop or an integrated pipeline tool can sufficiently run your workflow, it's likely that you may wish to have a tool that can do things like monitor and track workflow runs, run workflows on remote or heterogeneous infrastructure, and implement more complex triggers and/or branching logic to your own workflows. In these instances, external orchestrator would be a good choice. 

In large organizations, it may also be the case that ML workflows have not been standardized on a given orchestration tool and different teams may use different technologies. lolpop provides an attractive solution over directly coding orchestrator logic into your wofklows. This makes orchestrators pluggable, and, ideally, users can then easily migrate workloads between orchestration tools with a simple configuration change. 

See the [PrefectOrchestrator](prefect_orchestrator.md) for an example of an orchestrator in action. 

## How to Write an Orchestrator

The intended use of an orchestrator is to implement it as a [decorator](using_custom_decorators.md) to your own workflow. To do this, users would need to write a decorator function that wraps methods in classes they wish to log to an orchestrator. This decorator is declared to lolpop, which dynamically applies it at runtime. Users are expected to be able to control various aspects of this behavior by standard integration configuration. 

Most modern python orchestrators provide a way to integrate via decorators into existing python code. If this is the case, then the lolpop decorator will more or less be a wrapper around the corresponding wrapper function in the orchestrator. If no such decorator integration exists for the orchestrator, then more work may need to be done in working w/ the orchestrator's python SDK. 

In addition to defining the decorator function, a lolpop orchestrator should implement `package`, `deploy`, `run`, and `stop` methods. These methods integrate with the lolpop [CLI](cli.md) and streamline building and running deployments in the orchestrator. More on this, below. 

## How to Use a Custom Orchestrator
Once an orchestrator has been written, they are easy to implement in existing lolpop workflows. You'll simply need to add the decorator to your config `yaml` file. 

```yaml hl_lines="10 11"
pipelines: 
  process: OfflineProcess 
  train: OfflineTrain
  predict: OfflinePredict
components: 
  metadata_tracker: MLFlowMetadataTracker
  notifier: StdOutNotifier
  resource_version_control: dvcVersionControl
  metrics_tracker: MLFlowMetricsTracker
decorators: 
  orchestrator: PrefectOrchestrator
... 

orchestrator: 
    config: 
        decorator_method: decorator
        integration_types: ["component", "pipeline", "runner"]
...

```
This now will apply your `decorator_method` in the orchestrator class to all classes of type in `integration-types` 

## Using Orchestrators with the lolpop CLI

The lolpop [CLI](cli.md) contains a `deployment` command which can build, deploy, and run workflows on external systems. Orchestrators is one of the mechanisms that can be used to accomplish this. Below we'll summarize how to use each command, but be sure to visit the [CLI reference](cli_reference.md) for all available options. 

### lolpop deployment package

In order to package a lolpop class with an orchestrator, you'll need to provide the Orchestrator class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for packaging via `-p` and any keyword arguments via `--packaging-kwargs`

```bash 
lolpop deployment package <lolpop_class> --packager <OrchestratorClass> -c /path/to/orchestrator_config.yaml -p <package_method> --packaging_kwargs {<dict_values>}
```

Typically, the expectation is that this creates something like a docker image that can then be deployed via `lolpop deployment build`.

### lolpop deployment build 

In order to deploy a packaged workflow, you'll need to provide the Orchestrator class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for deployment via `-d` and any keyword arguments via `--deployment-kwargs`

```bash 
lolpop deployment build --deployer <OrchestratorClass> -c /path/to/orchestrator_config.yaml -d <deployment_method> --deployment_kwargs {<dict_values>}
```

This action should create/register a deployment with the orchestrator for future use. 

### lolpop deployment run 

In order to run a deployed workflow, you'll need to provide the Orchestrator class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for run via `-r` and any keyword arguments via `--run-kwargs`

```bash 
lolpop deployment run <deployment_name> --deployer <OrchestratorClass> -c /path/to/orchestrator_config.yaml -d <run_method> --run_kwargs {<dict_values>}
```

This should create a workflow instance in the orchestrator. 

### lolpop deployment stop 

In order to stop a deployed workflow, you'll need to provide the Orchestrator class to use, along w/ the config file for that class. You can optionally provide the method in the class to use for run via `-s` and any keyword arguments via `--run-kwargs`

```bash 
lolpop deployment stop <deployment_name> --deployer <OrchestratorClass> -c /path/to/orchestrator_config.yaml -d <package_method> --stop_kwargs {<dict_values>}
```
