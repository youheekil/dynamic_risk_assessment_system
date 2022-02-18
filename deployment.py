import os
import json
import pickle
import shutil


# Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])
output_model_path = os.path.join(config['output_model_path'])

def store_model_into_pickle():
    """
    This function is for a deployment. Copying the latest pickle file, the latestscore.txt value,
    and the ingestfiles.txt into the deployment directory.
    # :param model: trained model
    :return:
    """
    # copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    # Source path
    # with open(model, 'wb') as file:
    #    pickle.dump(model, os.path.join(output_model_path, "trainedmodel.pkl"))

    model = os.path.join(output_model_path, "trainedmodel.pkl")
    score = os.path.join(output_model_path, "latestscore.txt")
    file_list = os.path.join("ingestedfiles.txt")

    source = [model, score, file_list]
    destination = prod_deployment_path

    # Copy the content of source to destination
    for s in source:
        dest = shutil.copy(s, destination)


if __name__ == "__main__":
    store_model_into_pickle()

