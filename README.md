Full Stack Casting Agency API Backend
About
This project provides an API to create and visualize a Casting Agency needs. Members can manage information about actors and movies.

LINK:
https://paragon-agency.herokuapp.com/

API
In order to use the API users need to be authenticated. Users will need to sign in an verify themselves to obtain a Token. An overview of the API can be found below.

Retrieves a list of all actors:
```
curl -X GET \
  https://paragon-agency.herokuapp.com/actors \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
GET /actors
```


Retrieves a list of all movies:
```
curl -X GET \
  https://paragon-agency.herokuapp.com/movies \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
GET /movies
```

Creates a new movie:
```
curl -X POST \
  https://paragon-agency.herokuapp.com/movies \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Transformers",
    "release_date": "2-25-2010",
POST /movies
```

Creates a new actor:
```
curl -X POST \
  https://paragon-agency.herokuapp.com/actors \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Dwayne Johnson",
    "age": 50,
    "gender": "Male"
}'
```

PATCH /movies/<id>
Change information for a given movie:
```
curl -X PATCH \
  https://paragon-agency.herokuapp.com/movies/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Jumanji"
}'
```



PATCH /actors/<id>
Change information for a given actor:
```
curl -X PATCH \
  https://paragon-agency.herokuapp.com/actors/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Kevin Hart"
}'
```

DELETE /movies/<id>
Delete a given movie:
```
curl -X DELETE \
  https://paragon-agency.herokuapp.com/movies/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \
```

DELETE /actors/<id>
Delete a given actor:
```
curl -X DELETE \
  https://paragon-agency.herokuapp.com/actors/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \
```

Installation
The following section explains how to set up and run the project locally.

Installing Dependencies
The project requires Python 3.8. Using a virtual environment such as pipenv is recommended. Set up the project as follows:

env/scripts/activate(to activate python env)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup
With Postgres running, create a database:
```bash
   sudo -u postgres createdb agency
```

## Running the server

First ensure you are working using your created virtual environment.

To run the server locally, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` file to find the application. 

__________________________________________________________________________________

Testing
To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb agency_test
python test_app.py
```