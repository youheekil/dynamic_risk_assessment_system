"""
Ingesting Data from multiple folders

Author: Youhee
Date: Feb 2022
"""


import os
import json
import logging
import pandas as pd
# from datetime import datetime

FORMAT = "%(asctime)s | %(name)s - %(levelname)s - %(message)s"
LOG_FILEPATH = "logs/testing.log/"
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    filemode='w',
    format=FORMAT)

# Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


def merge_multiple_dataframe():
    """
    Function for data ingestion, merging multiple dataframe
    Check for datasets, compile them together, and write to an output file
    :return:
    data: data frame of the ingested data
    """
    filenames = os.listdir(os.getcwd() + "/" + input_folder_path)
    df_list = pd.DataFrame(columns=['corporation', 'lastmonth_activity', 'lastyear_activity',
                                    'number_of_employees', 'exited'])
    for each_filename in filenames:
        try:
            df1 = pd.read_csv(os.path.join(os.getcwd(), input_folder_path, each_filename))
        except:
            logging.error("No columns to parse from file | %s", each_filename)
        else:
            df_list = df_list.append(df1)
            with open('ingestedfiles.txt', 'a') as f:
               f.write(f"{each_filename} \n")

    result = df_list.drop_duplicates()
    output_pth = os.path.join(output_folder_path, "finaldata.csv")
    result.to_csv(output_pth, index=False)
    return result


if __name__ == '__main__':
    merge_multiple_dataframe()
