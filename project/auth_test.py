import unittest
import json
from server import app, db
import os
from flask.testing import FlaskClient

client = app.test_client()
login_user = json.dumps({
                "email": "a@e.c",
                "password": "aaaa"
                
        })

response = client.post('/api/login/' , headers={"Content-Type": "application/json"}, data=login_user)

print(response.json)
print(response.headers)
response3 = client.get('/api/group/', headers={"Content-Type": "application/json"})

print(response3.json)