# Django OAuth2 Client Demo

This is a simple application with basic integration to a backend API that uses OAuth2.0 to provide permission on its resource data.

Please see the backend counterpart, first. (https://github.com/ricouly21/django_oauth2_demo)

## Installation

1. Rename ```django_oauth2client_demo/.env.copy``` into ```django_oauth2client_demo/.env``` and replace these values.
```
# API Server Details
API_URL = <Backend host name and/or port (ex: http://127.0.0.1:8000)>
CLIENT_ID = <The ID of your application>
CLIENT_SECRET = <The secret key of your application>
CLIENT_USER = <Username of Resource Owner>
CLIENT_PASSWORD = <Password of Resource Owner>
GRANT_TYPE = <Grant type of your application (ex: password)>
```

2. Enter these commands on your terminal to run the app:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0:8000
```

## Contributors
* ULY Rico

