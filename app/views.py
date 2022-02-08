from app import app
from markupsafe import escape
from flask import request, render_template, jsonify
import json
import os
import diagnostics
from IPython.display import HTML

with open('config.json','r') as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config['output_folder_path'])
production_deployment_path = os.path.join(config['prod_deployment_path'])

# Route to home page
@app.route("/<name>")
def index(name):
	return f"Hello, {name}!"

# Prediction Endpoint
@app.route("/prediction", methods=['GET','OPTIONS'])
def predict():
    pred = diagnostics.model_predictions()
    return str(pred)


# Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def scoring():
    with open(os.path.join(production_deployment_path, "latestscore.txt"), 'r') as file:
        f1 = file.readline().strip()
    return str(f1)


@app.route("/summarystats", methods =['GET', 'OPTIONS'])
def summary_stats():
	summary_df = diagnostics.dataframe_summary()
	return jsonify(summary_df.to_dict(orient="records"))


@app.route("/model_diagnostic", methods =['GET', 'OPTIONS'])
def model_diag():
	timing = diagnostics.execution_time()
	na_percent = diagnostics.missing_data()
	dependencies_check = diagnostics.outdated_packages_list()
	return timing + "\n" + na_percent + "\n" + dependencies_check