# Dynamic Risk Assessment System 

## Files
* `training.py`: a Python script meant to train an ML model
* `scoring.py`: a Python script meant to score an ML model
* `deployment.py`: a Python script meant to deploy a trained ML model
* `ingestion.py`: a Python script meant to ingest new data
* `diagnostics.py`: a Python script meant to measure model and data diagnostics
* `reporting.py`: a Python script meant to generate reports about model metrics
* `app.py`: a Python script meant to contain API endpoints
* `wsgi.py`: a Python script to help with API deployment
* `apicalls.py`: a Python script meant to call your API endpoints
* `fullprocess.py`: a script meant to determine whether a model needs to be re-deployed, 
and to call all other Python scripts when needed

## Code
```shell
pip install -r requirements.txt
```

|1. Data Ingestion|
```shell
python ingestion.py
```

|2. Training|
```shell
python training.py
```

|3. Scoring, deployment|
```shell
python scoring.py
python deployment.py
```

