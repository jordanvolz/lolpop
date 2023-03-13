from lolpop.runner import ClassificationRunner

#create runner from config
config_file = "/Users/jordanvolz/github/lolpop/examples/classification/main_local.yaml"
clf_runner = ClassificationRunner(config_file)
#run data processing
train_data, train_dataset_version = clf_runner.process_data()
##load data from disk for testing purposes to speed up workflow
#import pandas as pd
#data = pd.read_csv("/tmp/artifacts/new_data.csv")
#print(data.head())
#train model
model_version, model, deploy_model = clf_runner.train_model(train_data)
##skip training to speed up workflow 
#mv_id = "projects/c2-testing/environments/production/models/petfinder_adoption_speed/versions/cg5o5vcha9ts83rf6so0"
#model_version = clf_runner.metadata_tracker.run.model_versions.get(mv_id)
#deploy_model = True
if deploy_model: 
    clf_runner.deploy_model(model_version)
#run prediction
#model = None 
eval_data, eval_dataset_version = clf_runner.process_data(source_data="eval")
data, prediction_job = clf_runner.predict_data(model_version, model, eval_data, eval_dataset_version)
#evaluate ground truth
clf_runner.evaluate_ground_truth(prediction_job)

#exit
clf_runner.stop()
print("exiting...")