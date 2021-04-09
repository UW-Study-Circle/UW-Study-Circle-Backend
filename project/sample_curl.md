Add a user: 

```
curl -d '{
    "username": "akshat", 
    "password": "aaaa",
    "email": "a@e.c",
    "lastname": "Akshat",
    "firstname": "Sinha",
    "gender": "Male",
    "phonenumber": "123456789",
    "bday": "28-01-1995"
    }' -H 'Content-Type: application/json' 127.0.0.1:6969/api/user/
```

Delete a user:

```
curl -X "DELETE" 127.0.0.1:6969/api/user/id/3
```

Find a user: 

```
curl 127.0.0.1:6969/api/user/email/a@e.c
```