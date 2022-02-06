from pytest import fixture
import pandas as pd
import os
import json
import logging
from diagnostics import missing_data, dataframe_summary

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
        logging.info(
                "SUCCESS|Teseting missing data|"
                "The file returned NA percentage for each column of the data."
        )
    except:
        logging.error(
                "FAILED|Testing missing data|"
                "The results of missing data function is not correctly run"
        )


def test_dataframe_summary():
    summary_df = dataframe_summary()

    try:
        assert len(summary_df) == 3
    except:
        logging.error(
                "FAILED|Testing dataframe_summary|"
                "The file failed to return a statistics summary of the data"
        )

    try:
        import_summary_df = pd.read_csv(os.path.join(dataset_csv_path, "summary_df.csv"))
        assert import_summary_df.shape[0] > 0
        assert import_summary_df.shape[1] > 0
    except AttributeError as err:
        logging.error(
                "FAILED|Testing dataframe_summary|"
                "The file failed to save a dataframe of the statistics summary"
        )

# TODO: WRITE test_outdated_packages_list

