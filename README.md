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
## Populate Test data
```bash
python populate_data.py
```
## Seeing All Data
```python
from server import db, app
from models import User, Group
from werkzeug.security import generate_password_hash, check_password_hash

app.app_context().push()
User.query.all()
Group.query.all()
```
## Test Coverage
```shell
coverage run --branch combination_test.py
```
![coverage](https://user-images.githubusercontent.com/56054533/116767431-b2fdef00-a9f5-11eb-8b75-b9ac3b20998a.PNG)

