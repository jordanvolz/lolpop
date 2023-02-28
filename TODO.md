0. Code Review (check formatting, base to child params, inputs/output types, etc)
00. pipeline extensibility
00.1 i.e. using metaflow as pipeline instead of default pipelines
1. CLI
1.1. runner/pipeline/component templates
2. packaing strategy/requirements.txts
3. testing frameworking/strategy
3.1. tests for runners/components/pipelines
3.2. generic tests (like swapping components) that apply broadly
3.3. config based tests. I.E. you can define stuff in yamls. 
3.4 for testing purposes, might make sense to have test_build=True param in init that initializes components w/ valid configs
otherwise we might run into a complicated testing nightmare w/ cascading dependencies, etc 
4. Default Values
5. Flush out Logging/Notifications, revisit/refactor utils/abstract classes
6. Additional Use Case Examples: regression, time series analsis, NLP
7. Additional Components/integrations
7.1 mlflow, w&b metadata tracking
8. Orchestrator integrations/examples 
8.1 implementing runner code directly in orchestrator wrapper vs defining an orchestrator runner. I.E. AirflowRunner
8.1 prefect, dagster, airflow
9. CI/CD strategy
10. Compute layer. Where do things run? Should consider in the context of orchestrators. We don't want to do the orchestration, so possibly we can offload this to them.  
11. Object caching? Helps when re-running long pipelines. 
12. working w/ secrets managers
13. runner loading is slow --> look into
XX. Comparison w/ ZenML/kebro/ploomer/mlflow pipelienes/metaflow, etc