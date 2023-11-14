# PrefectOrchestrator Class

The `PrefectOrchestrator` class extends the `BaseOrchestrator` class and provides methods for working with Prefect. 

It will likely most commonly be used as an orchestrator applied to existing lolpop workflows. See [working with orchestrators](working_with_orchestrators.md) for more information on how this works. 

A secondary use is to leverage the lolpop [cli](cli.md) to package, build, and run deployments via Prefect. 


## Configuration

### Required Configuration 

The `PrefectOrchestrator` class has no required configuration. 

### Optional Configuration

The `PrefectOrchestator` has the following optional configuration:

- `prefect_settings` (dict): A dictionary of key-value pairs to apply the `prefect_profile` being used.  
- `task-kwargs` (dict): A dictionary of key-value pairs to  pass into the prefect task object when wrapping lolpop methods. 

### Default Configuration

The `PrefectOrchestator` has the following default configuration:

- `decorator_method` (str): The method which should be used as the decorator when applying the prefect orchestrator to a lolpop workflow. Defaults to "decorator" and likely should not be changed. 
- `integration_types` (str): A list of lolpop integration types to apply the `decorator_method` to. Defaults to `["runner", "pipeline", "component"]`
- `prefect_profile` (str): The prefect profile to use. Defaults to "default". This is largely for development purposes; in production we expect environment variables will be set.     
- `prefect_flow_integration` (list): A list of lolpop integrations, whose methods should be considered to be flows. Defaults to`["runner", "pipeline"]`.
- `prefect_task_integration` (list): A list of lolpop integrations, whose method should be considered to be tasks. Defaults to `["component"]`.
- `flow_kwargs` (dict): A dictionary of key-value arguments to pass into the prefect flow object when wrapping lolpop methods. Defaults to `{"log_prints": True}`, which will log lolpop dialog into prefect if it's using the `StdoutLogger`.
- `cache_tasks` (bool): Whether to cache tasks in prefect or now. Defaults to True.
## Methods

### decorator
Decorates a function with Prefect flow or task.

```python 
decorator(self, func, cls)
```

**Arguments**:

- func (object): The function to decorate.
- cls (object): The class containing the function.

**Returns**:
The decorated function.


### package 
Packages the Prefect flow into a Docker image or any other supported packaging format.

```python 
package(self, lolpop_class=None, lolpop_module=None, ..., *args, **kwargs)
```

**Arguments**:

  - `lolpop_class` (str): Name of the lolpop class to package.
  - `lolpop_module` (str): Name of the lolpop module to package.
  - `lolpop_entrypoint` (str): Name of the lolpop entrypoint to package.
  - `flow_name` (str): Name of the Prefect flow.
  - `package_type` (str): Packaging format for the Prefect flow (default: "docker").
  - `base_image` (str): Base Docker image for building the Docker image (default: "prefecthq/prefect:2-python3.9").
  - `prefect_files` (str): Folder containing the Prefect files.
  - `copy_files` (list): Files in the base directory to be copied to the Docker image.
  - `lolpop_install_location` (str): Installation location for the lolpop package.
  - `run_cmd` (str): Command to run at the end of the Docker file.
  - `config_file` (str): Path to the config file.
  - `flow_kwargs` (dict): Additional keyword arguments for the Prefect flow.
  - `dockerfile_path` (str): Path to the Dockerfile for a custom image when creating a Prefect deployment. Defaults to "Dockerfile".
  - `docker_image_tag` (str): Tag to apply to the Docker image after creation.
  - `push_image` (bool): Whether to push the image after creation. Defaults to False.
  - `skip_validation` (bool): Whether to skip component validation when loading the config file in the entrypoint script.
  - `create_deployment` (bool): Whether to use a proper Prefect deploy method. Defaults to False.
  - `work_pool` (str): Workpool name associated with this package.
  - `job_variables` (dict): Additional variables to be passed into the flow deployment to override the base deployment template.
  - `*args` and `**kwargs`: Additional positional and keyword arguments.

**Returns**:

  - None


### deploy 
Deploys the Prefect flow.

```python 
deploy(self, deployment_name, deployment_type="docker", ..., *args, **kwargs)
```


**Arguments**:

  - `deployment_name` (str): Name of the deployment to create.
  - `deployment_type` (str, optional): Type of deployment to create. Defaults to "docker".
  - `work_pool` (str, optional): Name of the work pool to deploy into. Defaults to None.
  - `flow_class` (str, optional): The flow class to deploy. Only used if a work pool is used. Defaults to None.
  - `flow_entrypoint` (str, optional): The flow entry point. Only used if a work pool is used. Defaults to None.
  - `docker_image_name` (str, optional): The Docker image name to use in the deployment, if using a custom image. Defaults to None.
  - `k8s_deployment_manifest` (str, optional): Path to the Kubernetes deployment manifest to use if deployment_type is "kubernetes". Defaults to None.
  - `dockerfile` (str, optional): Path to the Dockerfile for building a deployment with a custom image. Defaults to "Dockerfile".
  - `push_image` (bool, optional): Whether to push the image after creation. Only used if deploying a custom image. Defaults to False.
  - `job_variables` (dict, optional): Other job variables to pass into the flow deploy method to override the default template. Defaults to {}.
  - `secret_name` (str, optional): Name of the Kubernetes secret holding the Prefect secrets. Only used if deploying into Kubernetes. Defaults to "prefect-secrets".
  - `num_replicas` (int, optional): Number of replica pods to deploy. Only used if deploying into Kubernetes. Defaults to 1.
  - `prefect_api_key` (str, optional): Name of the Prefect API key secret in secret_name. Defaults to "prefect-api-key".
  - `prefect_api_url` (str, optional): Name of the Prefect API URL secret in secret name. Defaults to "prefect-api-url".
  - `image_pull_policy` (str, optional): Image pull policy to use in the Kubernetes deployment manifest. Defaults to "Never".
  - `manifest_path` (str, optional): Path to a Kubernetes deployment manifest. Only used if deploying into Kubernetes and if you wish to use a custom manifest file. Defaults to "prefect_files/deployment_manifest.yaml".
  - `namespace` (str, optional): Kubernetes namespace to deploy into. Only used if deploying into Kubernetes. Defaults to "lolpop".
  - `worker_image` (str, optional): Image to use for the Prefect Kubernetes worker. Defaults to "prefecthq/prefect:2-python3.9-kubernetes".
  - `worker_deployment_manifest` (str, optional): Manifest to use for the Prefect Kubernetes worker. Defaults to "prefect_files/worker_deployment_manifest.yaml".
  - `flow_kwargs` (dict, optional): Keyword arguments to pass into the flow instantiation. Defaults to {}.
  - `deployment_kwargs` (dict, optional): Keyword arguments to pass into the deployment instantiation. Defaults to {}.
  - `*args` and `**kwargs`: Additional positional and keyword arguments.

**Returns**
  - None


### run 
Runs a Prefect deployment.

```python 
run(self, deployment_name, *args, **kwargs)
```


**Arguments**:

- `deployment_name` (str): The deployment name to run.
- `*args` and `**kwargs`: Additional positional and keyword arguments.

**Returns**

- (flow_id, url): A tuple containing the flow ID and the URL of the flow run.


### stop 
Shuts down a current Prefect deployment.

```python
stop(self, deployment_name, deployment_type="docker", ..., *args, **kwargs)
```

**Arguments**:

- deployment_name (str): The deployment name to shut down.
- deployment_type (str, optional): The type of deployment. Defaults to "docker".
- docker_image_name (str, optional): The image name used in the deployment. Defaults to None.
- *args and **kwargs: Additional positional and keyword arguments.

**Returns**:
None

### _make_entrypoint_script 
Creates an entrypoint script to use in the Docker image.

```python
_make_entrypoint_script(self, flow_name="prefect_entrypoint", ...)
```

**Arguments**:

- `flow_name` (str, optional): Name of the flow. Defaults to "prefect_entrypoint".
- `lolpop_module` (str): The Lolpop module name. Defaults to "lolpop.runner".
- `lolpop_class` (str): The Lolpop class name.
- `lolpop_entrypoint` (str): The Lolpop entry point name. Defaults to "build_all".
- `config_file` (str): Path to the configuration file. Defaults to "prefect_files/dev.yaml".
- `flow_kwargs` (dict): Additional keyword arguments for the flow.
- `prefect_files` (str): Path to the Prefect files. Defaults to "prefect_files".
- `create_deployment` (bool): If True, creates a deployment. Defaults to False.
- `skip_validation` (bool): If True, skips configuration validation. Defaults to False.
- `work_pool` (str): Name of the work pool. Defaults to None.
- `job_variables` (dict): Additional job variables to pass.
- `docker_image_name` (str): Name of the Docker image. Defaults to None.
- `docker_image_tag` (str): Tag for the Docker image. Defaults to "latest".
- `dockerfile` (str): Path to the Dockerfile. Defaults to "Dockerfile".

**Returns**

- Path to the generated entrypoint script.

### _maker_dockerfile 
Creates a Dockerfile that sets up lolpop and executes the entrypoint script.

```python 
_make_dockerfile(self, base_image="prefecthq/prefect:2-python3.9", ...)
```

 **Arguments**:

  - `base_image` (str): Base Docker image. Defaults to "prefecthq/prefect:2-python3.9".
  - `prefect_files` (str): Path to the Prefect files. Defaults to "prefect_files/".
  - `copy_files` (list): Files to copy into the Docker image. Defaults to an empty list.
  - `lolpop_install_location` (str): Installation location for Lolpop package. Defaults to "'lolpop[cli,prefect,mlflow,xgboost]'".
  - `run_cmd` (str): Command to run the entrypoint script. Defaults to "lolpop prefect_files/run.py".
  - `dockerfile_path` (str): Path to save the Dockerfile. Defaults to "Dockerfile".

**Returns**:

- Path to the generated Dockerfile.

### _make_deployment_manifest 
Creates a deployment manifest for the lolpop Docker image.
  
```python 
_make_deployment_manifest(self, manifest_path="prefect_files/deployment_manifest.yaml", ...)
```


**Arguments**:

- `manifest_path` (str): Path for the deployment manifest. Defaults to "prefect_files/deployment_manifest.yaml".
- `deployment_name` (str): Name of the deployment. Defaults to "lolpop-prefect".
- `namespace` (str): Kubernetes namespace. Defaults to "lolpop".
- `num_replicas` (int): Number of replicas. Defaults to 1.
- `flow_name` (str): Name of the flow (must be provided).
- `image` (str): Image to use (must be provided).
- `image_pull_policy` (str): Image pull policy. Defaults to "Never".
- `prefect_secret_name` (str): Prefect secrets' name. Defaults to "prefect-secrets".
- `key_prefect_api_url` (str): Key for the Prefect API URL. Defaults to "prefect-api-url".
- `key_prefect_api_key` (str): Key for the Prefect API key. Defaults to "prefect-api-key".

**Returns**:

- Path to the generated manifest.

### _make_worker_deployment_manifest 
Creates a manifest for the Prefect worker.

```python 
_make_worker_deployment_manifest(self, manifest_path="prefect_files/worker_deployment_manifest.yaml", ...)
```


**Arguments**:

- Similar to `_make_deployment_manifest`.
- Additionally:
    - `work_pool` (str): The work pool (must be provided).
    - `service_account` (str): Service account name. Defaults to "default".

**Returns**:
  - Path to the generated worker deployment manifest.

### _apply_secrets 
Applies Prefect secrets to Kubernetes.

```python 
_apply_secrets(self, secret_name, secret_dict, namespace="lolpop")
```


**Arguments**:

- `secret_name` (str): The name of the secret.
- `secret_dict` (dict): Dictionary of key-value pairs for the secret.
- `namespace` (str): Kubernetes namespace. Defaults to "lolpop".

- **Returns**:

- Creates and applies the secret to the specified namespace.

### _build_docker_image 
Builds the Docker image.

```python 
_build_docker_image(self, dockerfile_path="Dockerfile", docker_image_tag=None, push_image=False, docker_kwargs={})
```


**Arguments**:

- `dockerfile_path` (str): Path to the Dockerfile. Defaults to "Dockerfile".
- `docker_image_tag` (str): Tag for the Docker image.
- `push_image` (bool): Whether to push the image after creation. Defaults to False.
- `docker_kwargs` (dict): Additional Docker build arguments.

- **Returns**:

- Builds the Docker image and optionally pushes it.

## Example Usage 

Orchestrators are intended to be attached to lolpop workflows by specifying the orchestrator as a decorator the workflow config file. To do this, simply add something like the following into the relevant yaml file. 

```yaml title="dev.yaml"
...
decorators: 
    orchestrator: PrefectOrchestrator

orchestrator: 
    config: 
        prefect_profile: dev 
        #specify any config for PrefectOrchestrator here
...
```

## Using Prefect with the the lolpop deployment CLI

lolpop supports a variety of ways to run Prefect workflows. All methods involve decorating your workflow with the `PrefectOrchestrator` class. From that point you can proceed with one of the following methods: 

1. Independent of Prefect's built-in deployment tools. 

2. Using Prefect's deployments for static infrastructure. 

3. Using Prefect's deployments for dynamic infrastructure. 

Prefect details [two methods](https://docs.prefect.io/2.14.1/concepts/deployments/#two-approaches-to-deployments) to deployment workflows within prefect, using static or dynamic infrastructure. Either of these can be utilized, or users can roll their own, as described below. 


### Independent execution

Once a `PrefectOrchestator` decorator has been added to a workflow, users can simply [run the workflow](running_workflows.md) as normal. The workflow will log to prefect, either via the `prefect_profile` specified in the orchestrator configuration, or to the instance specified in the environment variable `PREFECT_API_URL`. 

This method of execution is meant to be a catch all to allow users to support any kind of execution mechanism they desire. 

Example: 
```python 
from lolpop.runner import ClassificationRunner

#config contains PrefectOrchestator as a decorator
runner = ClassificationRunner(conf="/path/to/my/config.yaml")

#running this method will log a flow into Prefect
runner.process_data()

... 
```

This if fundamentally no different than running any other workflow within lolpop. Simply by adding a little additional configuration, we can begin working with orchestrators, as desired.

lolpop's CLI contains a deployment command which allows users to start automating working with popular deployment tools. In particular, users can leverage `lolpop deployment` to package, deploy, and run workflows on external orchestrators, including Prefect. 

### Static Infrastructure

Prefect's static infrastructure is meant to be a way to run prefect workflows on long-lived infrastructure. To accomplish this, prefect `flows` can run on specified infrastructure via the `flow.serve` method. The flow will then communicate with the Prefect API to monitor for new work and submit any run results from completed flow runs. The main benefit of this is that it allows users to run workflows remotely simply by executing a simply CLI command: `prefect run deployment <deployment-name>`. 


=== "Docker"

    ```bash
    lolpop deployment package QuickstartRunner \
        -m prefect_files.quickstart_runner \
        -c prefect_files/quickstart.yaml \
        --packager PrefectOrchestrator \
        --packaging-kwargs '{"copy_files":["train.csv","test.csv", "process_titanic.py"],   "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, "docker_image_tag":"lolpop-quickstartrunner-build-all-serve"}}'

    lolpop deployment build \ 
        -c prefect_files/quickstart.yaml \
        --deployer PrefectOrchestrator  \
        --deployment-kwargs='{"docker_image_name":"lolpop-quickstartrunner-build-all-serve"}'

    lolpop deployment run \ 
        prefect-entrypoint/lolpop-quickstartrunner-build-all-serve
        -c prefect_files/quickstart.yaml \ 
        --deployer PrefectOrchestrator

    ```

=== "Kubernetes"

    ```bash
    lolpop deployment package QuickstartRunner \
        -m prefect_files.quickstart_runner \
        -c prefect_files/quickstart.yaml \
        --packager PrefectOrchestrator \
        --packaging-kwargs '{"copy_files":["train.csv","test.csv", "process_titanic.py"], "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, "docker_image_tag":"lolpop-quickstartrunner-build-all-serve"}'

    lolpop deployment build \
        -c prefect_files/quickstart.yaml \
        --deployer PrefectOrchestrator \
        --deployment-kwargs '{"flow_class":"prefect_files.run", "flow_entrypoint": "prefect_entrypoint","docker_image_name":"lolpop-quickstartrunner-build-all", "job_variables":{"image_pull_policy":"IfNotPresent", "namespace":"lolpop"}}' \
        -n 'lolpop-quickstartrunner-build-all-serve' \
        -t kubernetes
    
    lolpop deployment run \ 
        prefect-entrypoint/lolpop-quickstartrunner-build-all-serve
        -c prefect_files/quickstart.yaml \ 
        --deployer PrefectOrchestrator
    ```


In the example above, we run 3 separate commands to execute this workflow: 

- `lolpop deployment package`: This builds an entrypoint scirpt to the method provided by `-m`, the docker file, and docker image for our workflow. We must always specify the orchestrator class and config file here to use. lolpop will then load that class and execute the `package` method in that class, passing in all relevant arguments. Using the `create_deployment` flag tells `PrefectOrchestator` that we want to run this on remote infrastructure, so our docker image will serve the flow specified by `-m`. 

- `lolpop deployment build`: This deploys our docker image to the infrastructure specified by `deployment_type` (default is "docker"). Prefect will then know this is polling for work so any future submissions can be run on this infrastructure. We must always provide the orchestrator class and config file here. lolpop will then load that class and execute the `deploy` method in that class, passing in all relevant arguments. 

- `lolpop deployment run`; This kicks off a flow run. Users must provide an orchestrator class and config file. lolpop will then load that class and execute the `run` method in that class, passing in all relevant arguments. This is essentially a thin wrapper around `prefect deployment run` for the `PrefectOrchestator`. 

The parameters needed for each command will depend greatly on the infrastructure the workflow is running on. The example above shows an example for docker and kubernetes deployment using the [classification quickstart example](classification_quickstart.md). Other examples or infrastructures should follow similarly.

### Dynamic Infrastructure

Prefect's dynamic infrastructure deployment mechanism is useful for cases where dedicated infrastructure isn't available or needed for a workflow. In this example, Prefect allows users to create `work pools` to which users can submit flow runs. Prefect `workers` can join a workpool and will then start executing work as it is requested. Instead of creating a deployment via `flow.serve`, the dynamic infrastructure mechanism instead utilizes `flow.deploy` to build a deployment. This will build a docker image for the deployment and 


=== "Docker"

    ```bash
    prefect work-pool create lolpop-docker-pool --type docker

    lolpop deployment package QuickstartRunner \
        -m prefect_files.quickstart_runner \
        -c prefect_files/quickstart.yaml \
        --packager PrefectOrchestrator \
        --packaging-kwargs '{"copy_files":["train.csv","test.csv", "process_titanic.py"],   "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, "work_pool":"lolpop-docker-pool", "docker_image_tag":"lolpop-quickstartrunner-build-all"}}'

    prefect worker start --pool lolpop-docker-pool 

    lolpop deployment build \ 
        -c prefect_files/quickstart.yaml \
        --deployer PrefectOrchestrator  \
        --deployment-kwargs='{ "work_pool":"lolpop-docker-pool", "flow_class":"prefect_files.run", "flow_entrypoint": "prefect_entrypoint","docker_image_name":"lolpop-quickstart-runner-build-all", "deployment_kwargs":{"job_variables":{"image_pull_policy":"Never"}}}' -n 'lolpop-quickstartrunner-build_all'

    lolpop deployment run \ 
        prefect-entrypoint/lolpop-quickstartrunner-build-all
        -c prefect_files/quickstart.yaml \ 
        --deployer PrefectOrchestrator

    ```

=== "Kubernetes"

    ```bash

    prefect work-pool create lolpop-k8s-pool --type kubernetes 

    lolpop deployment package QuickstartRunner \
        -m prefect_files.quickstart_runner \
        -c prefect_files/quickstart.yaml \
        --packager PrefectOrchestrator \
        --packaging-kwargs '{"copy_files":["train.csv","test.csv", "process_titanic.py"], "lolpop_install_location":"prefect_files/lolpop-testing.tar.gz[cli,prefect,mlflow,xgboost]", "config_file":"prefect_files/quickstart.yaml", "skip_validation":true, "create_deployment":true, 
        "work_pool":"lolpop-k8s-pool", "docker_image_tag":"lolpop-quickstartrunner-build-all-serve"}'

    lolpop deployment build \
        -c prefect_files/quickstart.yaml \
        --deployer PrefectOrchestrator \
        --deployment-kwargs '{"work_pool":"lolpop-k8s-pool", "flow_class":"prefect_files.run", "flow_entrypoint": "prefect_entrypoint","docker_image_name":"lolpop-quickstartrunner-build-all", "job_variables":{"image_pull_policy":"IfNotPresent", "namespace":"lolpop"}}' \
        -n 'lolpop-quickstartrunner-build-all' \
        -t kubernetes
    
    lolpop deployment run \ 
        prefect-entrypoint/lolpop-quickstartrunner-build-all
        -c prefect_files/quickstart.yaml \ 
        --deployer PrefectOrchestrator
    ```

The 3 `lopop` command above are used similarly to the static infrastructue example, with a few differences: 

- lolpop assumes you already have a work pool created for use. 

- Since prefects `flow.deploy` will build a docker image when called, `lolpop deployment package` will skip the image building step when a `work_pool` is specified. 

