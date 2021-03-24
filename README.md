## Dev Setup
 - Install Virtualenv
 ```bash
 sudo pip3 install virtualenv
 ```
 - Create virtualenv folder
 ```bash
python3 -m venv env
 ```
 Activate Virtualenv
 ```bash
 source env/bin/activate
 ```
 Install requirements
 ```bash
 pip3 install -r requirements.txt
 ```
 Deactivate Virtualenv
 ```bash
deactivate
```
## Run Server
```shell
python run.py
```


## Seeing All Data
```python
from server import db, app
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

app.app_context().push()
user1 = User(username='Peter', email='peter@e.c', password=generate_password_hash('p'))
user2 = User(username='Ash', email='ash@e.c', password=generate_password_hash('a'))

db.session.add(user1)
db.session.add(user2)
db.session.commit()
User.query.all()
```
