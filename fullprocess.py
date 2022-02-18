import json
import os
from itertools import chain
import ingestion as _ingestion
import training as _training
import scoring as _scoring
import deployment as _deployment
import diagnostics as _diagnostics
import reporting as _reporting
import apicalls as _apicalls
import logging
FORMAT = "%(asctime)s | %(name)s - %(levelname)s - %(message)s"
LOG_FILEPATH = "logs/testing.log/"
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    filemode='a',
    format=FORMAT)

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

prod_deployment_path = os.path.join(config['prod_deployment_path'])
input_folder_path = os.path.join(config['input_folder_path'])
model_path = os.path.join(config['output_model_path'])

def execute_fullprocess():
    # Check and read new data
    # first, read ingestedfiles.txt
    with open(os.path.join(prod_deployment_path, "ingestedfiles.txt")) as file:
        current_data = list(chain(*[line.split() for line in file.readlines()]))

    # second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
    new_data_list = os.listdir(os.getcwd() + "/" + input_folder_path)

    # Deciding whether to proceed, part 1
    # if you found new data, you should proceed. otherwise, do end the process here

    if current_data not in new_data_list:
        _ingestion.merge_multiple_dataframe()
        _scoring.score_model(prod=True)
    else:
        exit(0)

    # Checking for model drift
    # check whether the score from the deployed model is different from the score
    # from the model that uses the newest ingested data
    with open(os.path.join(model_path, "latestscore.txt"), 'r') as new_score:
        new_f1 = float(new_score.read())

    with open(os.path.join(prod_deployment_path, "latestscore.txt"), "r") as old_score:
        old_f1 = float(old_score.read())


    # Deciding whether to proceed, part 2
    # if you found model drift, you should proceed. otherwise, do end the process here

    if new_f1 >= old_f1:
        logging.info("NO MODEL DRIFT IS DETECTED| Actual F1 (%s) is better/equal than old F1 (%s)" % (new_f1, old_f1))
    else:
        logging.warning("MODEL DRIFT IS DETECTED| Actual F1 (%s) is WORSE than old F1 (%s) -> training model" % (new_f1, old_f1))
        _training.train_model()
        _deployment.store_model_into_pickle()

    # Re-deployment
    #if you found evidence for model drift, re-run the deployment.py script

    # Diagnostics and reporting
    # run diagnostics.py and reporting.py for the re-deployed model
    _diagnostics.model_predictions()
    _diagnostics.execution_time()
    _diagnostics.dataframe_summary()
    _diagnostics.missing_data()
    _diagnostics.outdated_packages_list()
    _reporting.score_model()
    _apicalls.apicalls()


if __name__ == "__main__":
    execute_fullprocess()

