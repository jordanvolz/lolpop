0. Code Review (check formatting, base to child params, inputs/output types, etc)
xx--> change src --> lolpop -- DONE 
--> docstrings -- IN PROGRESS
--> pre-commit hook for python formatting
xx--> change all __init__ calls to use keyword args only. This allows for easier inheritance and multiple inheritence as other classes can super().__init__ and just pass all **kwargs -- DONE
xx00. mlflow integration -- DONE
xx000. pipeline extensibility
xx00.1 i.e. using metaflow as pipeline instead of default pipelines -- DONE
1. CLI
xx1.1. runner/pipeline/component templates -- DONE
xx1.2 Project templates -- DONE
xx1.3 Need to think more about custom runner/pipeline/component packaging/installation. Might be good to have lolpop/adapters/<component/pipeline/runner> and then in lolpop/<component/pipeline/runner> we add that to the dir/path. This would then give a bath for people to build then our and install from binary into site-packages/lolpop. --DONE 
2. packaging strategy/setup.py/requirements.txts
xx--> poetry setup -- DONE 
--> try to use extras_require to pull in individual requirements.txt from components?
xx--> cli in pypi package -- DONE
--> idea is that users can package up their own stuff, i.e. add component and create binary, or docker image, or even docker image of embedded model, etc. 
--> but also need to work through distributing lolpop's defaults
--> Note; issue w/ evidently requiring pyyaml <6 and dbt-core >=6, currently can install via `pip3 install -e . --no-deps` to get by it. 
2.1 project structure? 
--> best practice is probably to be opinionated about this and then have an easy packaging mechanism in the CLI. 
--> this would make non-unit workflow testing less confusing too, very likely.
xx2.2 Plugin support -- done 
3. testing frameworking/strategy
3.1. tests for runners/components/pipelines
3.2. generic tests (like swapping components) that apply broadly
3.3. config based tests. I.E. you can define stuff in yamls. 
3.4 for testing purposes, might make sense to have test_build=True param in init that initializes components w/ valid configs. otherwise we might run into a complicated testing nightmare w/ cascading dependencies, etc 
3.5 dbt-style data tests
4. Default Values
5. Flush out Logging/Notifications, revisit/refactor utils/abstract classes
6. Additional Use Case Examples: regression, time series analsis, NLP
7. Additional Components/integrations
xx7.1 mlflow, 
7.2 w&b
7.3 ml model support? sklearn/pytorch
8. Orchestrator integrations/examples 
8.1 implementing runner code directly in orchestrator wrapper vs defining an orchestrator runner. I.E. AirflowRunner
8.1 prefect, dagster, airflow
9. CI/CD strategy
10. Compute layer. Where do things run? Should consider in the context of orchestrators. We don't want to do the orchestration, so possibly we can offload this to them.  
i.e. do we need an 'operator' concept?
11. Object caching? Helps when re-running long pipelines. 
--> idea is to define things you want to cache in decorators and then also have a caching component
12. working w/ secrets managers
xx13. runner loading is slow --> look into. -- DONE 
--> profiling via: https://stackoverflow.com/questions/16373510/improving-speed-of-python-module-import
    --> gist is that some of the libaries we are importing are very slow 
xx--> also suppress import messaging when loading lolpop
xx14. Data synthesizer + data seeding for better local experience -- DONE 
15. Notebook to lolpop component conversions
    --> some interesting tools in this space. see for example: https://github.com/kubeflow-kale/kale
16. ChatGPT to write documentation of your workflow. And maybe docstrings/unit tests/etc?
17. visual dag of workflows/dependencies (networkx?) --> gets more into governance stuff
zz. Comparison w/ ZenML/kebro/ploomer/mlflow pipelines/metaflow/beam?/aqueduct, etc
--> would be good to map the concepts between metadata stores as well

To build, MVP: 
xx1. 1 Additional Pipeline Extension (MetaFlow? mlflow?) -- DONE
xx2. 1 Additional Metadata Tracker Extension (MLFlow? w&b) 
    -- MLFlow DONE
xx3. 2 Additional Data Integrations: (duckdb/bigquery/redshift/s3/gcs/databricks) -- DONE
4. 2 Additional Use Case Examples: (Regression/TS/Recommender/NLP)
5. Testing Framework
6. Project Templates -- WIP
7. MVP Documentation
xx8. Local Experience -- i.e. try it out w/o complicated installs/registrations
    -- DONE
xx9. MVP packaing -- pip install
    -- DONE 