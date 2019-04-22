# Admission forms - Backend

## Initialization

Before any manipulations run:
* On Unix: 
```bash
export FLASK_APP=server.py
```
* On Windows: 
```bash
set FLASK_APP=server.py
set FLASK_ENV=development
```

## Run server

Go to home folder:
```bash
cd /home/dilshatsalih/adminssion-forms-backend/
```

Activate virtualenv:
```bash
source ../ssd_new_1/bin/activate
```

In foreground:
```bash
flask run --host=0.0.0.0
```

In background
```bash
nohup flask run --host=0.0.0.0 &
```

## Deployment

Run:
```bash
git pull
pip install -r requirements.txt
flask db upgrade
```

## Migrations

Create migration: `flask db migrate`  
Apply migration: `flask db upgrade`  
