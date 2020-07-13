# Django OAuth2 Client Demo

This is a simple application with basic integration to a backend API that uses OAuth2 for authentication and permission to data.

Please see the backend counterpart, first. (https://github.com/ricouly21/django_oauth2_demo)

## Installation
1. Run these commands to run the app:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations accounts
python manage.py runserver
```

2. Edit these values on ```mysite/views.py``` to connect to your own copy of the backend server.
```
api_url = "http://127.0.0.1:8080"
client_id = "<your_client_application_id>"
client_secret = "<your_client_secret>"
grant_type = "password"
client_user = "<your_client_username>"
client_password = "<your_client_password>"
```

## Contributors
* ULY Rico

