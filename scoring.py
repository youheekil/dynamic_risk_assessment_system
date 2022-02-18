from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f)

model_path = os.path.join(config['output_model_path'])
dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])

# Function for model scoring
def score_model(prod):
    """
    This function takes a trained model, load test data, and calculate on F1 score for the model
    relative to the test data
    :param prod:
    prod = True means we are getting finaldata
    prod = False means we are getting test data
    :return:
    f1 score value
    """
    # loading the trained model
    with open(os.path.join(prod_deployment_path, 'trainedmodel.pkl'), 'rb') as file:
        model = pickle.load(file)

    if prod == True:
        # importing finaldata.csv
        df = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    else:
        # importing test data
        df = pd.read_csv(os.path.join(test_data_path, "testdata.csv"))
    X_test = df.drop(columns = ['corporation', 'exited']).values
    y_test = df['exited'].values

    pred = model.predict(X_test)
    f1 = f1_score(pred, y_test)

    # record the result of the f1_score to the latestscore.txt file
    with open(os.path.join(model_path, 'latestscore.txt'), 'w') as file:
        file.write(f"{f1}\n")
    return f1


if __name__ == "__main__":
    score_model(prod=True)