# square_database_structure

## about

database structure layer for my personal server.

## installation

```shell
pip install square_database_structure
```

## usage

### to add a new database

- create a package with package name as database name.

### to add a new schema

- add package in database_name package with schema name as package name.

### to add a new table

- create /database_name/schema_name/tables.py file if not already created.
- create class corresponding to your new table add in /database_name/schema_name/tables.py file.

### to add default data in table

- append row objects containing your default data to the data_to_insert list inside the
  /database_name/schema_name/tables.py file.

## env

- python>=3.12.0

## changelog

### v1.0.2

- replace file_purpose with app_id in file_storage.

### v1.0.1

- add main.py file to have explicit mapping and ordering for schemas to be created.
- move database and schema names to __init__.
- add app table in public, change user, remove profile and add user app and remove enums.

### v1.0.0

- initial commit

## Feedback is appreciated. Thank you!
