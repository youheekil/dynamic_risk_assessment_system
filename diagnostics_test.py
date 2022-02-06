from pytest import fixture
import pandas as pd
import os
import json
import logging
from diagnostics import missing_data

FORMAT = "%(asctime)s | %(name)s - %(levelname)s - %(message)s"
LOG_FILEPATH = "logs/testing.log/"
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    filemode='a',
    format=FORMAT
)


# Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f)
dataset_csv_path = os.path.join(config['output_folder_path'])

@fixture
def import_data():
    try:
        final_data = pd.read_csv(os.path.join(dataset_csv_path, "finaldata.csv"))
    except FileNotFoundError as err:
        logging.error(
                "Testing Import_data is failed | The data is not found successfully"
        )
    return final_data


def test_missing_data(import_data):
    data = import_data
    try:
        na_percentage = missing_data()
        assert len(na_percentage) == len(data.columns)
    except:
        logging.error(
                "Testing missing data is failed |"
                "The results of missing data function is not correctly run"
        )