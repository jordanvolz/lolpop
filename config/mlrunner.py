from runner import ClassificationRunner

config_file = "/home/jordanvolz/mlops-jumpstart/config/main.yaml"
clf_runner = ClassificationRunner(config_file)
#data = clf_runner.process_data()
##load data from disk for testing purposes to speed up workflow
import pandas as pd
data = pd.read_csv("/tmp/artifacts/new_data.csv")
print(data.head())
model = clf_runner.train_model(data)
print("exiting...")
exit()
new_data = clf_runner.process_data()
predictions = clf_runner.predict_data(model,new_data)