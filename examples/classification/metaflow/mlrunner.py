from lolpop.runner import MetaflowClassificationRunner

#create runner from config
config_file = "/Users/jordanvolz/github/lolpop/examples/classification/metaflow/metaflow_local_dev.yaml"
runner = MetaflowClassificationRunner(config_file)

#run data processing
train_data, train_dataset_version = runner.process_data()

#train model
model_version, model, deploy_model = runner.train_model(train_data)
if deploy_model: 
    runner.deploy_model(model_version, model)

#run prediction
eval_data, eval_dataset_version = runner.process_data(source_data="eval")
data, prediction_job = runner.predict_data(model_version, model, eval_data, eval_dataset_version)

#evaluate ground truth
runner.evaluate_ground_truth(prediction_job)

#exit
runner.stop()
print("exiting...")