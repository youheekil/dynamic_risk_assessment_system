"""
Diagnostics

author: Youhee
Date: Feb 2022
"""
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess

from training import trim_data

# Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])

def model_predictions():
    """
    This function is to get model predictions.
    Read the deployed model and a test dataset. Then predictions will be calculated.
    :return:
    prediction : a list of all predictions values
    """
    # Read the deployed model and a test dataset
    with open(os.path.join(prod_deployment_path, "trainedmodel.pkl"), 'rb') as file:
        model = pickle.load(file)

    # read test data
    X_test, y_test = trim_data(data_path = os.path.join(test_data_path, "testdata.csv"))

    # Calculate predictions
    pred = model.predict(X_test)

    return pred


def dataframe_summary():
    """
    This function is to get summary statistics (mean, median, sd).
    :return:
    summary_statistics : a list containing all summary statistics
    """
    data = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    numerical_col = data.select_dtypes(include=np.number).columns.tolist()
    X_numeric = data[numerical_col]

    # calculate summary statistics here
    for col in X_numeric.columns:
        mean = np.mean(col)
        median = np.median(col)
        std = np.std(col)
    # TODO: I don't know how to store list for the summary statistics


def missing_data():
    """
    This function is to check for missing data.
    It will return a list with the same number of elements as the number of columns in your dataset.
    :return:
    na_percentage : a list containing the percent of NA values in the data
    """
    # read the ingested final data
    data = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))

    # count the number of NA values in each column for the dataset.
    nas = list(data.isna().sum())
    # calculate what percent of each column consists of NA values.
    na_percentage = [nas[i] / len(data.index) for i in range(len(nas))]

    return print(na_percentage)

def ingestion_timing():
    starttime = timeit.default_timer()
    os.system('python3 ingestion.py')
    timing=timeit.default_timer() - starttime
    return timing


def training_timing():
    starttime = timeit.default_timer()
    os.system('python3 training.py')
    timing = timeit.default_timer() - starttime
    return timing


def execution_time():
    """
    This function is to measure timing for ingestion function and
    trianing function
    :return:
    timing : a list containing two timing values in seconds
    """
    # calculate timing of training.py and ingestion.py
    timing = []
    timing.append(ingestion_timing())
    timing.append(training_timing())
    return print(timing)


def outdated_packages_list():
    """
    This function is to check dependencies getting a list of outdated packages.
    It will output a table with three columns:
    the first column will show the name of a Python module that you're using,
    the second column will show the currently installed version of that Python module,
    and the third column will show the most recent available version of that Python module.
    :return:
        dependencies_list : A table containing list of python modules
    """

    dependencies = subprocess.check_output(['pip', 'list', '--outdated'], text = True)
    with open('installed.csv', 'w') as file:
        file.write(dependencies)

    dependencies_list = pd.read_csv("installed.csv")
    package = []; installed_version = []; available_version = []
    for idx in range(1, len(dependencies_list)):
        a = list(dependencies_list.iloc[idx])[0]
        b = " ".join(a.split())
        l = b.split()
        package.append(l[0])
        installed_version.append(l[1])
        available_version.append(l[2])

    os.remove("installed.csv")
    dependencies_table = pd.DataFrame(list(zip(package, installed_version, available_version)),
                                      columns=['package', 'installed_version', 'available_version'])
    dependencies_table.to_csv("dependencies.csv", columns=['package', 'installed_version', 'available_version'])
    return print(dependencies_table.head(10))

if __name__ == '__main__':
    model_predictions()
    # dataframe_summary()
    execution_time()
    missing_data()
    outdated_packages_list()





    
