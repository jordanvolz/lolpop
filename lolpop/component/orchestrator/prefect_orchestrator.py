from lolpop.component.orchestrator.base_orchestrator import BaseOrchestrator
from lolpop.utils import common_utils as utils
from functools import wraps
import os 
import json 
from importlib import import_module

@utils.decorate_all_methods([utils.error_handler])
class PrefectOrchestrator(BaseOrchestrator): 

    __DEFAULT_CONF__ = {
        "config": {
            "decorator_method": "decorator",
            "integration_types": ["runner", "pipeline", "component"], 
            "prefect_profile": "default",
            "prefect_flow_integration": ["runner", "pipeline"], 
            "prefect_task_integration": ["component"],
            "flow_kwargs": {"log_prints": True}, 
            "cache_tasks": True,
        }
    }

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        # check to see if env variables are set. 
        # in prefect env variables override profiles and are set in the root context so
        # there is no (non-super hacky) current way to override them programatically
        # but we can at least provide a warning
        prefect_env_variables = [x for x in os.environ.keys() if x.startswith("PREFECT")]
        if len(prefect_env_variables)>0: 
            self.log("Found PREFECT_* configuration in the environment variables: %s. Environment variables override profile settings in Prefect. Consider unsetting these variables if their use is not intended." %str(prefect_env_variables), level="INFO")

        # we need to switch profiles before importing prefect. The reason being that prefect
        # sets the root context when imported to the active profile. The only way to change this
        # programatically is via prefect.context.use_profile and some context manager acrobatics, 
        # which is going to be complicated for lolpop. It's easier to just execute a profile switch
        profile = self._get_config("PREFECT_PROFILE")
        out, _ = utils.execute_cmd(["prefect", "profile", "use", profile], logger=self)

        #if profile is new, then try to create it and apply settings
        if "not found" in out: 
            utils.execute_cmd(
                ["prefect", "profile", "create", profile], logger=self)

            profile_settings = self._get_config("prefect_settings", {})
            for k, v in profile_settings.items():
                utils.execute_cmd(
                    ["prefect", "config", "set", f"{k}={v}"], logger=self)

        self.log("Using prefect profile %s" %profile, level="INFO")

        #now we can import, and we'll also need to add them to globals
        from prefect import flow, task 
        globals()["flow"] = flow 
        globals()["task"] = task 

    def decorator(self, func, cls):
        """
        Decorates a function with Prefect flow or task.

        Args:
            func (object): The function to decorate.
            cls (objcet): The class containing the function.

        Returns:
            The decorated function.
        """
        @wraps(func)
        def prefect_wrapper(*args, **kwargs):
            obj = args[0]
            #wrap in flow
            if obj.integration_type in self._get_config("prefect_flow_integration"):
                flow_kwargs = self._get_config("flow_kwargs", {})
                #note: the integration_framework object creates a "maximum recursion depth exceeded" error in prefect
                # prefect calls prefect._vendors.fastapi.encoders.jsonable_encoder on parameters you pass into your flow
                # for complex stuff this usually errors out and is handled safely, but the anytree object doesn't error
                # and it seems it gets stuck in a child -> parent -> child loop until it breaks. So, we'll just remove it here.
                # this should be safe, as the integration_framework is really only used during __init__ calls and is otherwise
                # a cosmetic feature
                if hasattr(obj, "integration_framework"):
                    delattr(obj, "integration_framework")
                return flow(func, **flow_kwargs)(*args, **kwargs)  # noqa: F821
            #wrap in task
            elif obj.integration_type in self._get_config("prefect_task_integration"):
                try: #skip wrapping things that are sub components. This will cause nested task error in prefect
                    if obj.parent_integration_type == "component": 
                        raise Exception("Detected task in a task. This is not allowed in prefect, so we'll attempt to run the function as normal.")
                    task_kwargs = self._get_config("task_kwargs",{})
                    cache_key_fn = None
                    if self._get_config("cache_tasks"):
                        from prefect.tasks import task_input_hash 
                        cache_key_fn = task_input_hash
                    return task(func, cache_key_fn = cache_key_fn, **task_kwargs)(*args,**kwargs)  # noqa: F821
                except Exception as e: 
                    return func(*args, **kwargs)
            else: #func gets decorated but it shouldn't be, do what's normal
                return func(*args, **kwargs)
        return prefect_wrapper
    
    def package(self, 
                lolpop_class=None,
                lolpop_module=None,
                lolpop_entrypoint="build_all",
                flow_name="prefect_entrypoint",
                package_type="docker",
                base_image="prefecthq/prefect:2-python3.9", 
                prefect_files="prefect_files/",
                copy_files=None,
                lolpop_install_location="'lolpop[cli,prefect,mlflow,xgboost]'",
                run_cmd = None,
                config_file=None,
                flow_kwargs=None,
                dockerfile_path="Dockerfile",
                docker_image_tag=None,
                push_image=False,
                skip_validation=False,
                create_deployment=False,
                work_pool = None, 
                job_variables = None,
                *args, **kwargs):

        """
        Packages the Prefect flow into a Docker image or any other packaging format supported by Prefect.

        Args:
            lolpop_class (str): The name of the lolpop class to package.
            lolpop_module (str): The name of the lolpop module to package.
            lolpop_entrypoint (str): The name of the lolpop entrypoint to package.
            flow_name (str): The name of the Prefect flow.
            package_type (str): The packaging format for the Prefect flow (default: "docker").
            base_image (str): The base Docker image to use for building the Docker image (default: "prefecthq/prefect:2-python3.9").
            prefect_files (str): The folder containing the Prefect files.
            copy_files (list): The files in the base directory to be copied to the Docker image.
            lolpop_install_location (str): The installation location for the lolpop package.
            run_cmd (str): The command to run the at the end of the docker file.
            config_file (str): The path to the config file.
            flow_kwargs (dict): Additional keyword arguments for the Prefect fkiw
            dockerfile_path (str): Path to the dockerfile to use for a custom image when creating a prefect deployment. Defaults to "Dockerfile",
            docker_image_tag (str): Tag to apply to the docker image after creation.
            push_image (bool): Whether to push the image after creation. Defaults to False.
            skip_validation (bool): Whether to skip component validation on the when loading the config file in the entrypoint script.
            create_deployment (bool): Whether to use a proper prefect deploy method. Defaults to False,
            work_pool (str): The workpool name associated with this package.  
            job_variables (str): Additional variables to be passed into the flow deployment to override the base deployment template. 
        """
        if flow_kwargs is None: 
            flow_kwargs = {}
        if copy_files is None: 
            copy_files = [] 
        if job_variables is None: 
            job_variables = {} 

        self.log("Building entrypoint script for prefect flow...")

        if config_file is None: 
            config_file = f"{prefect_files}/dev.yaml"

        if docker_image_tag is None:
            docker_image_tag = utils.get_docker_string(f"lolpop-{lolpop_class}-{lolpop_entrypoint}:latest")
        if ":" not in docker_image_tag:
            docker_image_tag = docker_image_tag + ":latest"

        #Note: for prefect we need to build a wrapper script that exposes the lolpop entrypoint. 
        #The reason for this is that prefect doesn't allow class methods to be entrypoints to a flow.
        #So, the flow entry point must be a just a standalone method. 
        #See https://github.com/PrefectHQ/prefect/discussions/9277 for more discussion on this. 
        entrypoint_script = self._make_entrypoint_script(
            flow_name=flow_name,
            lolpop_class=lolpop_class, 
            lolpop_module=lolpop_module,
            lolpop_entrypoint=lolpop_entrypoint, 
            config_file=config_file,
            prefect_files=prefect_files, 
            flow_kwargs=flow_kwargs, 
            skip_validation=skip_validation,
            create_deployment=create_deployment,
            work_pool=work_pool,
            job_variables=job_variables,
            docker_image_name=docker_image_tag.split(":")[0],
            docker_image_tag=docker_image_tag.split(":")[1],
            dockerfile=dockerfile_path,
            )

        self.log(f"Successfully built entrypoint script {entrypoint_script}")

        #we can now build a dockerfile w/ the correct entrypoint script. 
        #we need this regardless of if we're going to build the docker file now 
        #or later in a flow deploy method. 
        self.log("Building dockerfile...")

        if run_cmd is None:
            run_cmd = f"python {prefect_files}/run.py"

        dockerfile = self._make_dockerfile(
            base_image=base_image,
            prefect_files=prefect_files,
            copy_files=copy_files,
            lolpop_install_location=lolpop_install_location,
            run_cmd=run_cmd,
            dockerfile_path=dockerfile_path)

        self.log(f"Successfully built dockerfile {dockerfile}")
        
        if work_pool is None:

            docker_image_tag = utils.get_docker_string(docker_image_tag)
            self.log(f"Building docker image {docker_image_tag}...")

            docker_image = self._build_docker_image(
                dockerfile_path=dockerfile,
                docker_image_tag=docker_image_tag,
                push_image=push_image,
            )

            self.log(f"Successfully created docker image {docker_image_tag}!")
        else: 
            self.log(f"Detected work pool {work_pool}. Skipping docker build, as prefect will build an image during deployment.")

    def deploy(self, deployment_name, deployment_type="docker", work_pool=None,
               flow_class=None, flow_entrypoint=None,
               docker_image_name = None, k8s_deployment_manifest=None, dockerfile="Dockerfile",
               push_image=False, job_variables=None, secret_name="prefect-secrets", num_replicas=1, 
               prefect_api_key="prefect-api-key", prefect_api_url="prefect-api-url", 
               image_pull_policy="Never", manifest_path="prefect_files/deployment_manifest.yaml",
               namespace="lolpop", worker_image="prefecthq/prefect:2-python3.9-kubernetes", 
               worker_deployment_manifest="prefect_files/worker_deployment_manifest.yaml",
               service_account="default",
               flow_kwargs=None, deployment_kwargs=None, *args, **kwargs):
        """Deploys the prefect flow

        Args:
            deployment_name (str): Name of the deployment to create. 
            deployment_type (str, optional): Type of deploymen to create. Defaults to "docker".
            work_pool (str, optional): Name of the work pool to deploy into. Defaults to None.
            flow_class (str, optional): The flow class to deploy. Only used if work pool is used. Defaults to None.
            flow_entrypoint (str, optional): The flow entrypoint. Only used if work pool is used. Defaults to None.
            docker_image_name (str, optional): The docker image name to use in the deployment, if using a custom image. Defaults to None.
            k8s_deployment_manifest (str, optional): The path to the k8s deployment manifest to use, if deployment_type = kubernetes. Defaults to None.
            dockerfile (str, optional): The path to the dockerfile to use if building a deployment with a custom image. Defaults to "Dockerfile".
            push_image (bool, optional): Whether to push the image after creation. Only used if deploying a custom image. Defaults to False.
            job_variables (dict, optional): Other job variables to pass into the flow deploy method to override the default template. Defaults to {}.
            secret_name (str, optional): Name of the k8s secret holding the prefect secrets. Only used if deploying into k8s. Defaults to "prefect-secrets".
            num_replicas (int, optional): Number of replica pods to deploy. Only used if deploying into k8s. Defaults to 1.
            prefect_api_key (str, optional): The name of the prefect api key secret in secret_name. Defaults to "prefect-api-key".
            prefect_api_url (str, optional): The name of the prefect api url secret in secret name. Defaults to "prefect-api-url".
            image_pull_policy (str, optional): The image pull policy to use in the k8s deployment manifest.. Defaults to "Never".
            manifest_path (str, optional): Path to a k8s deployment manifest. Only used if deploying into k8s and if you wish to use a custom manifest file. Defaults to "prefect_files/deployment_manifest.yaml".
            namespace (str, optional): k8s namespace to deploy into. Onkly used if deploying into k8s. Defaults to "lolpop".
            worker_image (str, optional): The image to use for the prefect k8s worker. Defaults to "prefecthq/prefect:2-python3.9-kubernetes".
            worker_deployment_manifest (str, optional): The manifest to use for the prefect k8s worker. Defaults to "prefect_files/worker_deployment_manifest.yaml".
            flow_kwargs (dict, optional): kwargs to pass into the flow instatiation. Defaults to {}.
            deployment_kwargs (dict, optional): kwargs to pass into the deployment instatiation. Defaults to {}.

        Raises:
            Nothing
        """
        if flow_kwargs is None: 
            flow_kwargs = {}
        if deployment_kwargs is None: 
            deployment_kwargs = {}
        if job_variables is None: 
            job_variables = {}         

        if docker_image_name is not None:
            if ":" not in docker_image_name:
                docker_image_name = docker_image_name + ":latest"

        #if we have a workpool or deploying local then we'll use the prefect deployment mechanism
        if deployment_type=="local" or work_pool is not None: 
            if flow_class is None and flow_entrypoint is None: 
                raise Exception("flow_class and flow_entrypoint are None. They must be populated for deployment_type = 'local'.")

            from prefect import flow, Flow
            from prefect.deployments import DeploymentImage

            mod = import_module(flow_class)
            f = getattr(mod,flow_entrypoint)
            if not isinstance(f, Flow):
                f = flow(f, **flow_kwargs)
        
            if deployment_type == "local":
                f.serve(name=deployment_name, **deployment_kwargs)
            elif deployment_type == "docker": 
                if docker_image_name is not None: 
                    image_name, image_tag = docker_image_name.split(":")
                    f.deploy(name=deployment_name, work_pool_name=work_pool,  
                             image=DeploymentImage(name=image_name, tag=image_tag, dockerfile=dockerfile),
                             push=push_image, job_variables=job_variables, **deployment_kwargs)
                else: 
                    f.deploy(name=deployment_name, work_pool_name=work_pool, **deployment_kwargs)
            elif deployment_type == "kubernetes": 
                #make sure secrets are applied to k8s
                self._apply_secrets(secret_name, {
                    prefect_api_url: os.environ["PREFECT_API_URL"],
                    prefect_api_key: os.environ["PREFECT_API_KEY"]
                })

                if k8s_deployment_manifest is None:
                    #make deployment script for prefect worker
                    self.log("Building k8s deployment manifest for prefect worker...")

                    k8s_deployment_manifest = self._make_worker_deployment_manifest(
                        work_pool=work_pool, 
                        deployment_name=deployment_name,
                        namespace=namespace,
                        image=worker_image,
                        manifest_path=worker_deployment_manifest,
                        num_replicas=num_replicas, 
                        image_pull_policy=image_pull_policy,
                        prefect_secret_name=secret_name, 
                        key_prefect_api_key = prefect_api_key, 
                        key_prefect_api_url = prefect_api_url,
                        service_account=service_account,
                        )
                    self.log("Built k8s deployment manifest for prefect worker. Saved to %s." %k8s_deployment_manifest)
                    
                #apply deployment
                out, exit_code = utils.execute_cmd(["kubectl", "apply", '-f', k8s_deployment_manifest], logger=self)

                if exit_code==0: 
                    self.log(out)
                else: 
                    self.log("Applying the manifest %s failed. Please inspect the yaml file to determine any errors." %k8s_deployment_manifest)

                #deploy flow 
                if docker_image_name is not None: 
                    image_name, image_tag = docker_image_name.split(":")
                    f.deploy(name=deployment_name, work_pool_name=work_pool,  
                             image=DeploymentImage(name=image_name, tag=image_tag, dockerfile=dockerfile),
                             push=push_image, job_variables=job_variables, **deployment_kwargs)
                else: 
                    f.deploy(name=deployment_name, work_pool_name=work_pool, **deployment_kwargs)

        elif deployment_type=="docker": #no workpool, so we want to just serve the container in docker
            if docker_image_name is None: 
                raise Exception("docker_image_name is None. It must be provided for deployment_type=docker.")
            
            PREFECT_API_URL = f'PREFECT_API_URL={os.environ["PREFECT_API_URL"]}'
            PREFECT_API_KEY = f'PREFECT_API_KEY={os.environ["PREFECT_API_KEY"]}'
            utils.execute_cmd(["docker", "run", '-e', PREFECT_API_URL,'-e', PREFECT_API_KEY, docker_image_name], run_background=True, logger=self)

        elif deployment_type=="kubernetes": #no workpool, so we want to serve a container in k8s deployment
            if k8s_deployment_manifest is None: 
                self.log("Building k8s deployment manifest...")

                self._apply_secrets(secret_name, {
                                    prefect_api_url: os.environ["PREFECT_API_URL"], 
                                    prefect_api_key: os.environ["PREFECT_API_KEY"]
                                    })
                k8s_deployment_manifest = self._make_deployment_manifest(
                    flow_name=utils.get_docker_string(flow_entrypoint), 
                    deployment_name=deployment_name,
                    image=docker_image_name,
                    manifest_path=manifest_path,
                    num_replicas=num_replicas, 
                    image_pull_policy=image_pull_policy,
                    prefect_secret_name=secret_name, 
                    key_prefect_api_key = prefect_api_key, 
                    key_prefect_api_url = prefect_api_url,
                    )
                self.log("Built k8s deployment manifest. Saved to %s." %k8s_deployment_manifest)

            out, exit_code = utils.execute_cmd(["kubectl", "apply", '-f', k8s_deployment_manifest], logger=self)

            if exit_code==0: 
                self.log(out)
            else: 
                self.log("Applying the manifest %s failed. Please inspect the yaml file to determine any errors." %k8s_deployment_manifest)

        else: 
            raise Exception("Deployment type %s not supported for PrefectOrchestrator" %deployment_type)     


    def run(self, deployment_name, *args, **kwargs): 
        """Runs a prefect deployment. 

        Args:
            deployment_name (str): The deployment name to run.

        Returns:
            (flow_id, url): A tuple containing the flow id and the url of the flow run. 
        """

        if kwargs is not None and len(kwargs) > 0: 
            out, code = utils.execute_cmd(["prefect", "deployment", "run", deployment_name, "--params", json.dumps(kwargs)], logger=self)
        else: 
            out, code = utils.execute_cmd(["prefect", "deployment", "run", deployment_name], logger=self)
        
        try:
            flow_id = out.split("UUID:")[1].split("\n")[0].strip()
        except:
            flow_id = out 

        try: 
            url = out.split("URL:")[1].replace("\n","").strip()
        except: 
            url = ""
        return (flow_id, url) 


    def stop(self, deployment_name, deployment_type="docker", docker_image_name = None, *args, **kwargs): 
        """Shuts down a current prefect deployment

        Args:
            deployment_name (str): The deployment name to shut down
            deployment_type (str, optional): The type of deployment that it is. Defaults to "docker".
            docker_image_name (str, optional): The image name used in the deployment. Defaults to None.

        Returns:
            None
        """
        if deployment_type == "docker": 
            if docker_image_name is None: 
                raise Exception("docker_image_name not provided. This is required to stop the running docker container.")

            container_id, code = utils.execute_cmd(["docker", "ps", "-q", "--filter", "ancestor=%s" %docker_image_name], logger=self)

            if code !=0: 
                raise Exception("Error when trying to obtain container id.")
            
            if container_id is None or len(container_id) == 0: 
                self.log("Unable to find running container with image %s. The deployment was possibly already shut down?" %docker_image_name)
                return 
            
            container_id = container_id.strip()
            _, code = utils.execute_cmd(["docker", "stop", container_id], logger=self)

            if code == 0: 
                self.log("Successfully shut down container %s" %container_id)


        elif deployment_type == "kubernetes": 

            _, code = utils.execute_cmd(["kubectl", "delete", "deployment", deployment_name], logger=self)
            
            if code == 0:
                self.log("Successfully deleted deployment %s" % deployment_name)

        elif deployment_type == "local": 
            self.log("Local deployment consumes your terminal. Please find the window serving the prefect deployment and pushg Ctrl+C.") 

        else: 
            raise Exception("Deployment type %s unsupported." %deployment_type)


    # creates an entrypoint script to use in the docker image. 
    # this file gets saved into prefect_files/run.py
    def _make_entrypoint_script(self,
                                flow_name="prefect_entrypoint",
                                lolpop_module = "lolpop.runner",
                                lolpop_class = None,
                                lolpop_entrypoint = "build_all",
                                config_file="prefect_files/dev.yaml",
                                flow_kwargs=None, 
                                prefect_files = "prefect_files",
                                create_deployment=False,
                                skip_validation=False,
                                work_pool=None, 
                                job_variables=None, 
                                docker_image_name=None, 
                                docker_image_tag="latest", 
                                dockerfile="Dockerfile",
                                ): 
        if flow_kwargs is None: 
            flow_kwargs = {} 
        if job_variables is None: 
            job_variables = {}

        if lolpop_class is None: 
            raise Exception("lolpop_class must not be None!")

        flow_kwargs_str = ""
        if len(flow_kwargs)>0: 
            for k,v in flow_kwargs: 
                flow_kwargs_str = flow_kwargs_str + f"{k}={v}, "

        import_text = f"import {lolpop_class}"
        if lolpop_module is not None: 
            import_text = f"from {lolpop_module} {import_text}"
            
        entrypoint = f"{flow_name}()"
        entrypoint_name = utils.get_docker_string(f'lolpop-{lolpop_class.lower()}-{lolpop_entrypoint}')
        if create_deployment: 
            entrypoint = f"{flow_name}.serve(name='{entrypoint_name}')"
            #if work_pool is not None: 
            #    entrypoint = f"{flow_name}.deploy(name='{entrypoint_name}', \
            #                    work_pool_name='{work_pool}', job_variables={job_variables}, \
            #                    image=DeploymentImage(name='{docker_image_name}', tag='{docker_image_tag}', dockerfile='{dockerfile}'),\
            #                    push=False)"
            
        entrypoint_script = f"""{import_text}
from prefect import flow 
from prefect.deployments import DeploymentImage 

@flow({flow_kwargs_str})
def {flow_name}():
    runner = {lolpop_class}(conf="{config_file}", skip_config_validation={skip_validation})
    runner.{lolpop_entrypoint}()
    runner.log("Workflow completed!")

if __name__ == "__main__":
    {entrypoint}
"""
        entrypoint_script_path = f"{prefect_files}/run.py"
        with open(entrypoint_script_path, "w+") as file:
            file.write(entrypoint_script)

        return entrypoint_script_path

    #makes a dockerfile that sets up lolpop and executes the entrypoint script
    def _make_dockerfile(self, 
                          base_image="prefecthq/prefect:2-python3.9",
                          prefect_files="prefect_files/",
                          copy_files=None,
                          lolpop_install_location="'lolpop[cli,prefect,mlflow,xgboost]'",
                          run_cmd="lolpop prefect_files/run.py",
                          dockerfile_path = "Dockerfile"):
        if copy_files is not None and len(copy_files) > 0:
            copy_files = "COPY %s ./" % " ".join(copy_files)
        else: 
            copy_files = ""

        dockerfile = f"""FROM {base_image}

WORKDIR /opt/prefect  
RUN mkdir prefect_files 
COPY {prefect_files} prefect_files/
{copy_files} 
RUN pip install {lolpop_install_location}

# Run our flow script when the container starts
ENV PYTHONPATH=$PYTHONPATH:/opt/prefect
CMD {json.dumps(run_cmd.split(" "))}
        """
        #write dockerfile
        with open(dockerfile_path, "w+") as file: 
            file.write(dockerfile)

        return dockerfile_path

    #create a deployment manifest for the lolpop docker image. 
    #This manifest will deploy the lolpop docker image into k8s
    def _make_deployment_manifest(self,
                                      manifest_path="prefect_files/deployment_manifest.yaml",
                                      deployment_name="lolpop-prefect", 
                                      namespace="lolpop",
                                      num_replicas=1,
                                      flow_name=None,
                                      image=None,
                                      image_pull_policy="Never",
                                      prefect_secret_name="prefect-secrets", 
                                      key_prefect_api_url="prefect-api-url", 
                                      key_prefect_api_key="prefect-api-key",
                                      ): 
        
        if flow_name is None or image is None: 
            raise Exception("flow_name and image are None. These must be provided in order to createa  manifest file.")

        deployment_manifest = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {deployment_name}
  namespace={namespace}
spec:
  replicas: {num_replicas}
  selector:
    matchLabels:
      flow: {flow_name}
  template:
    metadata:
      labels:
        flow: {flow_name}
    spec:
      containers:
      - name: flow-container
        image: {image}
        env:
        - name: PREFECT_API_URL
          valueFrom: 
            secretKeyRef: 
              name: {prefect_secret_name} 
              key: {key_prefect_api_url}
        - name: PREFECT_API_KEY
          valueFrom: 
            secretKeyRef: 
              name: {prefect_secret_name} 
              key: {key_prefect_api_key}
        imagePullPolicy: {image_pull_policy}
"""
        #write manifest
        with open(manifest_path, "w+") as file:
            file.write(deployment_manifest)

        return manifest_path

    #Create a manifest for the prefect worker. 
    #This worker will pool the prefect server for work and run flows. 
    def _make_worker_deployment_manifest(self,
                                         manifest_path="prefect_files/worker_deployment_manifest.yaml",
                                         deployment_name="lolpop-prefect-worker",
                                         namespace="lolpop", 
                                         num_replicas=1,
                                         work_pool=None,
                                         image="prefecthq/prefect:2-python3.9-kubernetes",
                                         image_pull_policy="IfNotPresent",
                                         prefect_secret_name="prefect-secrets",
                                         key_prefect_api_url="prefect-api-url",
                                         key_prefect_api_key="prefect-api-key",
                                         service_account="default",
                                         ):
        if work_pool is None:
            raise Exception(
                "work_pool is None. This must be provided in order to createa  manifest file.")

        deployment_manifest = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {deployment_name}-{work_pool}
  namespace: {namespace}
spec:
  replicas: {num_replicas}
  selector:
    matchLabels:
      work_pool: {work_pool}
  template:
    metadata:
      labels:
        work_pool: {work_pool}
    spec:
      serviceAccountName: {service_account}
      containers:
      - name: prefect-worker
        image: {image}
        command: 
          - /usr/bin/tini
          - -g
          - -- 
          - /opt/prefect/entrypoint.sh
        args:
          - prefect
          - worker
          - start
          - --type
          - kubernetes
          - --pool 
          - {work_pool}
        env:
        - name: PREFECT_API_URL
          valueFrom: 
            secretKeyRef: 
              name: {prefect_secret_name} 
              key: {key_prefect_api_url}
        - name: PREFECT_API_KEY
          valueFrom: 
            secretKeyRef: 
              name: {prefect_secret_name} 
              key: {key_prefect_api_key}
        imagePullPolicy: IfNotPresent
"""
        #write manifest
        with open(manifest_path, "w+") as file:
            file.write(deployment_manifest)

        return manifest_path

    #apply prefect secrets to k8s
    def _apply_secrets(self, secret_name, secret_dict, namespace="lolpop"):
        
        secret_arr = ["kubectl", "create", "secret", "generic", secret_name, "--namespace", namespace]
        for k,v in secret_dict.items(): 
            secret_arr.append(f"--from-literal={k}={v}")
        utils.execute_cmd(["kubectl", "delete", "secret", secret_name,
                          "--ignore-not-found", "--namespace", namespace], logger=self)
        return utils.execute_cmd(secret_arr)

    #build the docker image
    def _build_docker_image(self,
            dockerfile_path="Dockerfile",
            docker_image_tag=None,
            push_image=False,
            docker_kwargs=None
    ): 
        if docker_kwargs is None: 
            docker_kwargs = {}
        if docker_image_tag is None: 
            raise Exception("docker_image_tag is None. Must provided a proper tag for the image.")
        
        if ":" not in docker_image_tag:
            docker_image_tag = docker_image_tag + ":latest"

        utils.execute_cmd(["docker", "build", "-t", docker_image_tag, "-f", dockerfile_path, "."],logger=self)

        if push_image: 
            utils.execute_cmd(["docker", "push", docker_image_tag], logger=self)
