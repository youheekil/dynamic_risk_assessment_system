import subprocess
from subprocess import DEVNULL, STDOUT, check_call
import json
import os
import requests
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


# Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f)
model_path = os.path.join(config['output_model_path'])

def apicalls():
    # Call each API endpoint and store the responses
    respond0 = requests.get('http://127.0.0.1:5000/youhee', headers=headers).text
    respond1 = requests.get('http://127.0.0.1:5000/prediction', headers=headers).text
    respond2 = requests.get('http://127.0.0.1:5000/score', headers=headers).text
    respond3 = requests.get('http://127.0.0.1:5000/summarystats', headers=headers).text
    respond4 = requests.get('http://127.0.0.1:5000/model_diagnostic', headers=headers).text

    with open(os.path.join(model_path, 'apireturns2.txt'), 'a') as file:
        file.write(str(respond0) + "\n")
        file.write(str(respond1) + "\n")
        file.write(str(respond2) + "\n")
        file.write(str(respond3) + "\n")
        file.write(str(respond4) + "\n")

    responses = {"greeting"    : respond0,
                 "prediction"  : respond1,
                 "scoring"     : respond2,
                 "summarystats": respond3,
                 "model diagnostic": respond4
                 }

    return print(responses)



if __name__ == '__main__':
    apicalls()

