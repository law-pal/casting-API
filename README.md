Full Stack Casting Agency API Backend
About
This project provides an API to create and visualize a Casting Agency needs. Members can manage information about actors and movies. 
My main motivation was to solidify all the concepts learned in this course, before doing the Nanodegree I didn't have any knowledge of technologies like FLASK, SQALchemy, and although not used in this particular project I was able to learn how to use Docker and Kubernetes, I am very excited that I was able to build a full functional API by myself also implementing AUTH0 as authentication is something I find very useful and definetely I will use it for future projects.

LINK:
https://paragon-agency.herokuapp.com/

API
In order to use the API users need to be authenticated also there's two open endpoints GET movies and GET actors. Users will need to sign in an verify themselves to obtain a Token. An overview of the API and Tokens for authentication can be found below.

```
Executive Producer has access to all endpoint and can modify all endpoints.
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9jMHQ1TVRrTllGeUhsX2NTcHVhNyJ9.eyJpc3MiOiJodHRwczovL2xhd3JlbmNlcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc0MDk0MDU5NTU4MTgxNzkyMDkiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9sYXdyZW5jZXAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwODM5NjE0OCwiZXhwIjoxNjA4NDgyNTQ4LCJhenAiOiJsclJUUkJib09scUxWTFl4U0N0bU4zbVQwN29VdFJ1QyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.fQOsrUVPazZifSL-zsrR35AS13mOFOTMJd7nCtl_mlRMABecTLxJjZCLBzxsk2TxSWBlOHZcpcguj6_tXYrFG8TSK-igjLbu2BT_wbvL98JE_25zeNPlQCQCvJVGhLLhlmRF-MG_UQ-JfqhCgOSd6nWho4CUulealq4bciJS34Y3nFtHjvBOGsKnNKy29pb05KKMG2QR560drlLCqYjf0CO_vqY1Uo3matgz5xn3q4eeaROu9eMjwf3Ge3ODXQ52_52KJgprxJJWZ1As3y0S2i59QnSNNRbmnPQ-IWXfiDFzoWge-dxBT64BBs80b1FiAnBy5Z3FJUZKCNWK6wVUgw'

```
```
Castin Director can GET movies and actors, PATCH actors and movies and only DELETE actors.
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9jMHQ1TVRrTllGeUhsX2NTcHVhNyJ9.eyJpc3MiOiJodHRwczovL2xhd3JlbmNlcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDgwMzMwMjk1OTgyOTg0NDA2MzkiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9sYXdyZW5jZXAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwODM5NjAwMCwiZXhwIjoxNjA4NDgyNDAwLCJhenAiOiJsclJUUkJib09scUxWTFl4U0N0bU4zbVQwN29VdFJ1QyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.VmIwbaA8vOC6aYwR26MYCSaiMlZKaEb9DoSRfXkfVA2pGV4DElBXWcRWxtidCfj88hMOIUhz0L30Wh0m0Gg9hCsZu-00qxp6X4K8eS6fF_8FKV26IsxugOSV2kUwkhIJVW_XMGd6z2AUlF2t-akcDebKTJCs4kInigZm3eS8CQYfaosJYLN9yfaJUZRn7VjpiU-dw9Ll2VehQ1zmDt0BgQA3pYrOMTHBeLdwiu7a1YCXKzbCAi6DbjygkElhPUgW55YxkgTyzy2DkWR0iS1_ofLPBYE1MkghUbbfPvyVJDNAxlfVxPLD999xLtFx42DDSFCimO-rBCBHrSZRu9puKQ'

```

```
Casting Assistant can only GET movies and actors.
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il9jMHQ1TVRrTllGeUhsX2NTcHVhNyJ9.eyJpc3MiOiJodHRwczovL2xhd3JlbmNlcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDk2MTg3NTMyMzY3Mjc1MTM3NTUiLCJhdWQiOlsiYWdlbmN5IiwiaHR0cHM6Ly9sYXdyZW5jZXAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwODM5NjA2NiwiZXhwIjoxNjA4NDgyNDY2LCJhenAiOiJsclJUUkJib09scUxWTFl4U0N0bU4zbVQwN29VdFJ1QyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.WxT2IUjBFiv90uxwbjxnChUATus3DMhDvh717ZsRZHjRcrYywpPftPAV6AbFSj-CcQrldis4mZIkL8Nm-xvw0leMxK9-CQ592s4ssW8t4bQk7Q296fSxZgYRE5Sc60qxK76oDhxXxi-Y7HVHUfsWy7mF2ON27lWJ_Q5n_PyThI6_h6grrNJVn2fQdxdevomQLux6khOILCRwpC--e2HSiwqRiIfYchU6NqNZiUP-OYm2ZNhOx0uU7BIIrgT1oGW1TV6JbxU5oa-IIHLN_5l-L9MogzPzSFYdlxSLD8RXIKrgsl--Oho8pDSChtEav_8eBB6GtnrLtGbsvAykK99lRQ'

```

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