from flask import Flask, session, jsonify, request
import json
import os

import diagnostics

with open('config.json','r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
production_deployment_path = os.path.join(config['prod_deployment_path'])

# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'


# greeting
@app.route('/')
def greeting():
    return "Welcome"

# Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():
    # call the prediction function you created in Step 3
    pred = diagnostics.model_predictions()
    return pred

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    #  debug=True, threaded=True
