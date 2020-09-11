# Django OAuth2 Client Demo

This is a simple application with basic integration to a backend API that uses OAuth2 for authentication and permission to data.

Please see the backend counterpart, first. (https://github.com/ricouly21/django_oauth2_demo)

## Installation
1. Run these commands to run the app:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0:8000
```

2. Rename ```django_oauth2client_demo/.env.copy``` into ```django_oauth2client_demo/.env``` and replace these values.
```
# API Server Details
API_URL=<backend_url_and_port>
CLIENT_ID=<your_client_application_id>
CLIENT_SECRET=<your_client_secret>
GRANT_TYPE=password
CLIENT_USER=<your_client_username>
CLIENT_PASSWORD=<your_client_username>
```

## Contributors
* ULY Rico

