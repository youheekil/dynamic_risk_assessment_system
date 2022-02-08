import joblib
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import warnings
warnings.filterwarnings("ignore")

# Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 
model_path = os.path.join(config['output_model_path'])
dataset_csv_path = os.path.join(config['output_folder_path']) # ingesteddata
test_data_path = os.path.join(config['test_data_path']) #testdata
prod_deployment_path = os.path.join(config['prod_deployment_path'])


# Function for reporting
def score_model():
    """
    This function is for reporting.
    Calculating a confusion matrix using the test data and the deployed model
    :return:
    """
    # importing test data and the deployed model
    with open(os.path.join(prod_deployment_path, "trainedmodel.pkl"), 'rb') as file:
        model = joblib.load(file)

    test_data = pd.read_csv(os.path.join(test_data_path, "testdata.csv"))
    X_test = test_data.drop(columns = ['corporation', 'exited']).values
    y_test = test_data['exited'].values

    pred = model.predict(X_test)

    # write the confusion matrix to the workspace
    plt.figure(figsize=[10, 8])
    cm = confusion_matrix(y_test, pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.savefig(os.path.join(model_path,'confusionmatrix.png'))
    plt.show()


if __name__ == '__main__':
    score_model()
