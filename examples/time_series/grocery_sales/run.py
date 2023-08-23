from lolpop.runner import TimeSeriesRunner

#create runner from config
config_file = "dev.yaml"
runner = TimeSeriesRunner(conf=config_file)

#run data processing
train_data, train_dataset_version = runner.process_data()

#train model
model_version, model, deploy_model = runner.train_model(train_data)
if deploy_model: 
    runner.deploy_model(model_version, model)

#run prediction
eval_data, eval_dataset_version = runner.process_data(source="eval")
data, prediction_job = runner.predict_data(
    model_version, model, eval_data, eval_dataset_version)

#evaluate ground truth
#runner.evaluate_ground_truth(prediction_job)

#exit
runner.stop()
print("exiting...")
