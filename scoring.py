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

trained_model_path = os.path.join(config['output_model_path'])
dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 


# Function for model scoring
def score_model():
    """
    This function takes a trained model, load test data, and calculate on F1 score for the model
    relative to the test data
    :return:
    f1 score value
    """
    # loading the trained model
    with open(os.path.join(trained_model_path, 'trainedmodel.pkl'), 'rb') as file:
        model = pickle.load(file)

    # importing test data
    test_data = pd.read_csv(os.path.join(test_data_path, "testdata.csv"))
    X_test = test_data.drop(columns = ['corporation', 'exited']).values
    y_test = test_data['exited'].values

    pred = model.predict(X_test)
    f1 = f1_score(pred, y_test)

    # record the result of the f1_score to the latestscore.txt file
    with open('latestscore.txt', 'a') as file:
        file.write(f"{f1}\n")
    return print(f1)


if __name__ == "__main__":
    score_model()