import requests

from django.shortcuts import render, redirect
from django.views.generic.base import View


api_url = "<backend_url_and_port>"
client_id = "<your_client_application_id>"
client_secret = "<your_client_secret>"
grant_type = "password"
client_user = "<your_client_username>"
client_password = "<your_client_password>"


class BlogView(View):
    template_name = "home.html"

    def get(self, request):
        user = request.session.get("USER")

        if user:
            context = {"user": user}
            return render(request, template_name=self.template_name, context=context)
        else:
            return redirect("login")


def index_view(request):
    return redirect("login")


def login_view(request):
    error_message = None

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


def logout_view(request):
    request.session["USER"] = None
    return redirect("login")


def authenticate(request):
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


def construct_headers(request):
    access_token = authenticate(request)
    return {"Authorization": "Bearer " + access_token}
