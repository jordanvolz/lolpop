from lolpop.extension import TimeSeriesRunner

#create runner from config
config_file = "/Users/jordanvolz/Downloads/ts_forecasting/config/duckdb_dev.yaml"
runner = TimeSeriesRunner(conf=config_file)

#run data processing
train_data, train_dataset_version = runner.process_data()

#train model
model, model_version, deploy_model = runner.train_model(train_data)
if deploy_model: 
    runner.deploy_model(model, model_version)

#run prediction
eval_data, eval_dataset_version = runner.process_data(source="eval")
data, prediction_job = runner.predict_data(
    model, model_version, eval_data, eval_dataset_version)

#evaluate ground truth
runner.evaluate_ground_truth(prediction_job)

#exit
runner.stop()
print("exiting...")
