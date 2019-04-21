# Admission forms - Backend

## Initialization

Before any manipulations run:
* On Unix: 
```
export FLASK_APP=server.py
```
* On Windows: 
```
set FLASK_APP=server.py
set FLASK_ENV=development
```

## Migrations

Create migration: `flask db migrate`  
Apply migration: `flask db upgrade`  
