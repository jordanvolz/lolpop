from runner import ClassificationRunner

#create runner from config
config_file = "/home/jordanvolz/lolpop/config/main.yaml"
clf_runner = ClassificationRunner(config_file)
#run data processing
#data = clf_runner.process_data()
##load data from disk for testing purposes to speed up workflow
import pandas as pd
data = pd.read_csv("/tmp/artifacts/new_data.csv")
print(data.head())
#train model
model_version, deploy_model = clf_runner.train_model(data)
print("deploy model?: %s" %deploy_model)
if deploy_model: 
    clf_runner.deploy_model(model_version)

print("exiting...")
exit()
#run prediction
new_data = clf_runner.process_data()
predictions = clf_runner.predict_data(model,new_data)