import requests

from django.shortcuts import render, redirect
from django.views.generic.base import View


api_url = ""
client_id = ""
client_secret = ""
grant_type = ""
client_user = ""
client_password = ""


class BlogView(View):
    template_name = "home.html"

    def get(self, request):
        return is_authenticated(request, self.template_name)


def index_view(request):
    return redirect("home")


def login_view(request):
    # Function to use for User login requests.
    # Automatically redirects to BlogView() on success.

    error_message = None

    # Check for existing User session.
    user = request.session.get("USER")
    if user:
        return index_view(request)

    # If no existing User session, proceed to default.
    if request.method == "POST":
        request_body = request.POST
        username = request.session["SAVED_USERNAME"] = request_body.get('username')
        email = username
        password = request_body.get('password')

        url = "{}/api/v1/users/get_user/".format(api_url)
        headers = construct_headers(request)
        payload = {
            "username": username,
            "email": email,
            "password": password,
        }

        resource = requests.post(url, json=payload, headers=headers)
        resource_data = resource.json()

        if resource.status_code == 200:
            user = request.session["USER"] = resource_data
            if user:
                return redirect("home")

        else:
            status_code = resource_data.get("status")
            error_message = resource_data.get("message")

    saved_username = request.session.get("SAVED_USERNAME") or ''

    return render(
        request,
        template_name="sign-in.html",
        context={
            "saved_username": saved_username,
            "error_message": error_message,
        }
    )


def sign_up_view(request):
    # Function to use for User sign-up requests.
    # Automatically redirects to BlogView() on success.

    error_message = None
    cached_form = {
        "username": '',
        "email": '',
        "first_name": '',
        "last_name": '',
    }

    # Check for existing User session.
    user = request.session.get("USER")
    if user:
        return index_view(request)

    # If no existing User session, proceed to default.
    if request.method == "POST":
        request_body = request.POST
        username = request_body.get('username')
        email = request_body.get('email')
        password1 = request_body.get('password1')
        password2 = request_body.get('password2')
        first_name = request_body.get('first_name')
        last_name = request_body.get('last_name')
        dob = request_body.get('dob')

        cached_form = request.session["SAVED_SIGNUP_FORM"] = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob
        }

        if password1 != password2:
            error_message = "ERROR: Passwords do not match."
            return render(
                request,
                template_name="sign-up.html",
                context={
                    "cached_form": cached_form,
                    "error_message": error_message,
                }
            )

        url = "{}/api/v1/users/create_user/".format(api_url)
        headers = construct_headers(request)
        payload = {
            "username": username,
            "email": email,
            "password": password1,
            "first_name": first_name,
            "last_name": last_name,
        }

        resource = requests.post(url, json=payload, headers=headers)
        resource_data = resource.json()

        if resource.status_code == 200:
            user = request.session["USER"] = resource_data
            account = create_account(request, user)
            if user:
                return redirect("home")

        else:
            status_code = resource_data.get("status")
            error_message = resource_data.get("message")

    return render(
        request,
        template_name="sign-up.html",
        context={
            "cached_form": cached_form,
            "error_message": error_message,
        }
    )


def logout_view(request):
    # Function to use for properly logging out.
    # Removes all session data using .flush()
    request.session.flush()
    return redirect("login")


def authenticate(request):
    # This function is used for requesting an access token.
    # The access token is then stored in the browser session for later use.
    # Returns a string.

    url = "{}/o/token/".format(api_url)

    payload = {
        "grant_type": grant_type,
        "username": client_user,
        "password": client_password,
    }

    auth = (client_id, client_secret)

    resource = requests.post(url, json=payload, auth=auth)
    resource_data = resource.json()

    request.session["API_SESSION"] = resource_data
    access_token = request.session["API_SESSION"]["access_token"]

    return access_token


def is_authenticated(request, redirect_to_template):
    # Function to check for existing User session.
    # If User session is valid, retrieves the User Account from user_id.
    # Automatically redirects to login view if no User session is found.

    user = request.session.get("USER")
    if user:
        account = request.session["ACCOUNT"] = get_account_from_user_id(request, user)
        context = {"account": account}
        return render(request, template_name=redirect_to_template, context=context)
    else:
        return redirect("login")


def get_account_from_user_id(request, user):
    # Function to retrieve an Account.
    # Requires a 'request' object and a 'user' object.
    # Returns a dict object, containing the Account details.

    url = "{}/api/v1/accounts/get_account_from_user_id/".format(api_url)
    headers = construct_headers(request)
    payload = {
        "user_id": user.get('id'),
    }

    resource = requests.post(url, json=payload, headers=headers)
    account = resource.json()

    return account


def create_account(request, user):
    # Function to create an Account.
    # Requires a 'request' object and a 'user' object.
    # Returns a dict object, containing the Account details.

    request_body = request.POST
    dob = request_body.get('dob')
    account = None

    if user:
        url = "{}/api/v1/accounts/create_account/".format(api_url)
        headers = construct_headers(request)
        payload = {
            "user_id": user.get('id'),
            "dob": dob,
        }

        resource = requests.post(url, json=payload, headers=headers)
        account = resource.json()

    return account


def construct_headers(request):
    # Helper function to create an authorization header for API requests.
    # Checks the browser session for an existing access token.
    # If no access token is found, calls 'authenticate()' function to request for a new one.
    # Returns a dict object, containing the access token.

    access_token = None
    api_session = request.session.get("API_SESSION")

    if api_session:
        access_token = api_session.get("access_token")

    if not access_token:
        access_token = authenticate(request)

    return {"Authorization": "Bearer " + access_token}








