from runner import ClassificationRunner

#create runner from config
config_file = "/Users/jordanvolz/github/lolpop/config/main_local.yaml"
clf_runner = ClassificationRunner(config_file)
#run data processing
data = clf_runner.process_data()
##load data from disk for testing purposes to speed up workflow
#import pandas as pd
#data = pd.read_csv("/tmp/artifacts/new_data.csv")
#print(data.head())
#train model
model_version, deploy_model = clf_runner.train_model(data)
##skip training to speed up workflow 
#mv_id = "projects/c2-testing/environments/production/models/petfinder_adoption_speed/versions/cfqo3tkha9tuq59hr0k0"
#model_version = clf_runner.metadata_tracker.run.model_versions.get(mv_id)
#deploy_model = True
print("deploy model?: %s" %deploy_model)
if deploy_model: 
    clf_runner.deploy_model(model_version)

print("exiting...")
exit()
#run prediction
new_data = clf_runner.process_data()
predictions = clf_runner.predict_data(model,new_data)