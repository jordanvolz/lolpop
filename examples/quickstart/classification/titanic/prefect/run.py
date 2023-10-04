from quickstart_runner import QuickstartRunner

#create runner from config
config_file = "prefect/quickstart.yaml"
runner = QuickstartRunner(conf=config_file, skip_config_validation=True)

#run data processing
train_data = runner.process_data()

#train model
model, model_version = runner.train_model(train_data)

#run prediction
eval_data = runner.process_data(source="eval")
data, _ = runner.predict_data(model, model_version, eval_data)

#view top predictions
print(data.head())

#exit
runner.stop()
print("exiting...")
