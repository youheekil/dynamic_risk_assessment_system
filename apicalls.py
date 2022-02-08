import subprocess
from subprocess import DEVNULL, STDOUT, check_call

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1/"

# curl http://127.0.0.1:5000/model_diagnostic

# Call each API endpoint and store the responses
respond = subprocess.run(['curl', '127.0.0.1:5000/prediction']).stdout
respond1 = subprocess.run(['curl', '127.0.0.1:5000/youhee']).stdout
respond2 = subprocess.run(['curl', '127.0.0.1:5000/scoring']).stdout
respond3 = subprocess.run(['curl', '127.0.0.1:5000/summarystats']).stdout


#combine all API responses
#responses = pass #combine reponses here

