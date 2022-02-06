

import pytest
import pandas as pd
import json
from ingestion import merge_multiple_dataframe
import os

import logging
FORMAT = "%(asctime)s | %(name)s - %(levelname)s - %(message)s"
LOG_FILEPATH = "logs/testing.log/"
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    filemode='a',
    format=FORMAT)


def test_merge_multiple_dataframe():
    """
    This is a function to test merge_multiple_dataframe.
    Checking if the file was correctly saved under `ingesteddata` folder.
    :return:
    None
    """

    # Load config.json and get input and output paths
    with open('config.json', 'r') as f:
        config = json.load(f)

    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']

    try:
        merge_multiple_dataframe()
        data = pd.read_csv(os.path.join(output_folder_path, "finaldata.csv"))

        assert data.shape[0] > 0
        assert data.shape[1] > 0
        logging.INFO("SUCCESS: The ingested data is successfully loaded")

    except AttributeError as err:
        logging.WARNING("FAILED: The file is not successfully loaded")
