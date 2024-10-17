Dev: 

python3 -m venv venv \
source bin/venv/activate \
pip install -r requirements.txt \
flask --app main run --host=0.0.0.0 --debug