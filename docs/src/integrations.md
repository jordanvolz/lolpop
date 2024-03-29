# Integration Overview

This guide will deep dive into using lolpop's pre-built components, pipelines, and runners. Depending on your use case, you may find these robust enough to use out of the box, usable with a few tweaks, or as inspiration as you begin building your own [extensions](extensions.md). 


## In this Section

Here's an index of built-in integrations: 

- Integrations: 
    - [BaseIntegration](base_integration.md)
- Components: 
    - [BaseComponent](base_component.md)
    - **Data Checkers**: 
        - [BaseDataChecker](base_data_checker.md)
        - [Deepchecks](deepchecks_data_checker.md)
        - [EvidentlyAI](evidentlyai_data_checker.md)
        - [Stumpy](stumpy_matrix_profiler.md)
    - **Data Connectors**: 
        - [BaseDataConnector](base_data_connector.md)
        - [BigQuery](bigquery_data_connector.md)
        - [Databricks](databricks_sql_data_connector.md)
        - [DuckDB](duckdb_data_connector.md)
        - [Google Cloud Storage](gcs_data_connector.md)
        - [Local](local_data_connector.md)
        - [Postgres](postgres_data_connector.md)
        - [Redshift](redshift_data_connector.md)
        - [S3](s3_data_connector.md)
        - [Snowflake](snowflake_data_connector.md)
    - **Data Profilers**:
        - [BaseDataProfiler](base_data_profiler.md)
        - [EvidentlyAI](evidentlyai_data_profiler.md)
        - [Sweetviz](sweetviz_data_profiler.md)
        - [tslumen](tslumen_data_profiler.md)
        - [YData](ydata_data_profiler.md )
    - **Data Splitter**: 
        - [BaseDataSplitter](base_data_splitter.md)
        - [Local](local_data_splitter.md)
    - **Data Synthesizers**: 
        - [BaseDataSynthesizer](base_data_synthesizer.md) 
        - [SDV](sdv_data_synthesizer.md)
    - **Data Transformers**: 
        - [BaseDataTransformer](base_data_transformer.md)
        - [Bigquery](bigquery_data_transformer.md)
        - [Databricks SQL](databricks_sql_data_transformer.md)
        - [dbt](dbt_data_transformer.md)
        - [DuckDB](duckdb_data_transformer.md)
        - [Local](local_data_transformer.md)
        - [Postgres](postgres_data_transformer.md)
        - [Redshift](redshift_data_transformer.md )
        - [Snowflake](snowflake_data_transformer.md)
    - **Generative AI Chatbots**: 
        - [BaseGenAIChatbot](base_genai_chatbot.md)
        - [OpenAI](openai_chatbot.md )
    - **Hyperparameter Tuners**: 
        - [BaseHyperparameterTuner](base_hyperparameter_tuner.md)
        - [Local](local_hyperparameter_tuner.md)
        - [Optuna](optuna_hyperparameter_tuner.md) 
    - **Loggers**: 
        - [BaseLogger](base_logger.md)
        - [File](file_logger.md)
        - [StdOut](stdout_logger.md)
    - **Metadata Trackers**: 
        - [BaseMetadataTracker](base_metadata_tracker.md)
        - [MLFlow](mlflow_metadata_tracker.md)
    - **Metrics Trackers:** 
        - [BaseMetricsTracker](base_metrics_tracker.md)
        - [MLFlow](mlflow_metrics_tracker.md)
    - **Model Bias Checker**: 
        - [BaseModelBiasChecker](base_model_bias_checker.md)
        - [AI Fairness 360](aifairness360_model_bias_checker.md)
    - **Model Checkers**: 
        - [BaseModelChecker](base_model_checker.md)
        - [Deepchecks](deepchecks_model_checker.md)
        - [EvidentlyAI](evidentlyai_model_checker.md)
    - **Model Explainers**: 
        - [BaseModelExplainer](base_model_explainer.md)
        - [Alibi](alibi_model_explainer.md)
    - **Model Repositories**: 
        - [BaseModelRespository](base_model_repository.md)
        - [MLFlow](mlflow_model_repository.md)
    - **Model Trainers**: 
        - [BaseModelTrainer](base_model_trainer.md)
        - [Prophet](prophet_model_trainer.md)
        - [XGBoost](xgboost_model_trainer.md)
    - **Model Visualizers**: 
        - [BaseModelVisualizer](base_model_visualizer.md)
        - [Prophet](prophet_model_visualizer.md)
        - [Yellowbrick](yellowbrick_model_visualizer.md)
    - **Notifiers**: 
        - [BaseNotifier](base_notifier.md)
        - [Gmail](gmail_notifier.md)
        - [SMTP](smtp_notifier.md)
        - [StdOut](stdout_notifier.md)
    - **Orchestrators**: 
        - [BaseOrchestrator](base_orchestrator.md)
        - [PrefectOrchestrator](prefect_orchestrator.md)
    - **Resource Version Control**: 
        - [BaseResourceVersionControl](base_resource_version_control.md)
        - [DVC](dvc_resource_version_control.md)
    - **Test Recorder**: 
        - [BaseTestRecorder](base_test_recorder.md)
        - [Local](local_test_recorder.md)
- Pipelines: 
    - [BasePipeline](base_pipeline.md) 
    - **Deploy**: 
        - [BaseDeploy](base_deploy.md)
        - [Offline Deploy](offline_deploy.md)
    - **Predict**: 
        - [BasePredict](base_predict.md)
        - [Offline Predict](offline_predict.md)
    - **Process**: 
        - [BaseProcess](base_process.md)
        - [Offline Process](offline_process.md)
    - **Train**: 
        - [BaseTrain](base_train.md)
        - [Offline Train](offline_train.md)
    - **Metaflow**: 
        - [Overview](metaflow_overview.md)
        - [Metaflow Offline Deploy](metaflow_offline_deploy.md) 
        - [Metaflow Offline Predict](metaflow_offline_predict.md)
        - [Metaflow Offline Process](metaflow_offline_process.md)
        - [Metaflow Offline Train](metaflow_offline_train.md)

- Runners:
    - [BaseRunner](base_runner.md)
    - **Classification**: 
        - [Classification Runner](classification_runner.md)
        - [Metaflow Classification Runner](metaflow_classification_runner.md)
    - **Regression**: 
        - [Regression Runner](regression_runner.md)
        - [Metaflow Regression Runner](metaflow_regression_runner.md )
    - **Time-Series**: 
        - [Time-Series Runner](timeseries_runner.md)