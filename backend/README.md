# Casting Agency Backend API

## Getting Started

### Installing Dependencies

Follow the instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Environment

We recommend working in a virtual environment whenever using python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Or you can directly follow below steps:
1. python -m venv venv
2. source venv/bin/activate (windows: source venv/Scripts/activate)

Then you can install the dependencies using below command:

pip install <package-name>

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite/postgres database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript object Signing and Encryption for JWTs. Useful for encoding, decoding and verifying JWTs.

## Running the Server

From within the ./src directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py
```

run the server, execute:

```bash
Flask run --reload
```

The `--reload` flag will detect the changes and restart server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:XXXXX`
    - `post:XXXXX`
    - `patch:XXXXX`
    - `delete:XXXX`
6. Create new roles for:
    - AAAAA
        - can `get:XXXXXX`
    - BBBBB
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the AAAAA role to one and BBBBB role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `casting-agency.postman_collection.json`
    - Right-clicking the collection folder for roles, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.

