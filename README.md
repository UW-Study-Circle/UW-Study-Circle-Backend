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
staff = User(name='Peter', role='staff', email='peter@e.c', password=generate_password_hash('p'))
admin = User(name='Ash', role='admin', email='ash@e.c', password=generate_password_hash('a'))

db.session.add(staff)
db.session.add(admin)
db.session.commit()
User.query.all()
```
