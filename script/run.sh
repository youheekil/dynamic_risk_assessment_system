VENV = venv
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
 python3 -m venv $(VENV)
 $(PIP) install -r requirements.txt

clean:
    rm -rf __pycache__
    rm -rf venv