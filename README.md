**Table of Contents**


## Configuring
Just create .env file in your user directory(~).
### .env file structure

````
# PROJECT SETTINGS
DEBUG = #Bool
PROJECT_NAME= #String
BACKEND_PORT= #Integer/String
BACKEND_HOST= #String(ip validation)
FIRST_SUPERUSER_EMAIL= #String(mail validation)
FIRST_SUPERUSER_PASSWORD= #String
# SECURITY SETTINGS
ACCESS_TOKEN_EXPIRE_MINUTES= #Integer/String
ENCRYPT_KEY= #String
# DATABASE SETTINGS
DATABASE_HOST= #String(ip validation)
DATABASE_PORT= #Integer/String
DATABASE_USER= #String
DATABASE_PASSWORD= #String
DATABASE_NAME= #String
````

## Installation

Project require [Python] to run and [PostgreSQL] as database.

```sh
git clone https://github.com/ctrl-kitty/fastapi-sqlmodel.git
cd cd fastapi-sqlmodel
python -m pip install requirements.txt
python init.py
```

## Running

Now you can run app simply type
```commandline
python main.py
```

[Python]: <https://www.python.org/>
[PostgreSQL]: <https://www.postgresql.org/>