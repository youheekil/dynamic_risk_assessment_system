from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

import logging
FORMAT = "%(asctime)s | %(name)s - %(levelname)s - %(message)s"
LOG_FILEPATH = "logs/testing.log/"
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    filemode='a',
    format=FORMAT)


# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path']) 


# Function for training the model
def train_model():
    """
    This function is for training the logistic regression.
    :return:
    None
    """
    # read data
    data = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    X_train = data.drop(columns = ['corporation', 'exited']).values
    y_train = data['exited'].values
    # X_train, X_test, y_train, y_test = train_test_split(X, y, 0.2, random_state=42)

    # the logistic regression for training
    logit = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)

    # fit the logistic regression to your data
    model = logit.fit(X_train, y_train)
    logging.info("Training and fitting the logistic model to your data is successfully completed")

    # write the trained model to your workspace in a file called trainedmodel.pkl
    filehandler = open( os.path.join(model_path, "trainedmodel.pkl"), 'wb')
    pickle.dump(model, filehandler)


if __name__ == "__main__":
    train_model()