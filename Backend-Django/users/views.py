import jwt
import json
import datetime
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import User


@require_http_methods(["POST"])
def signup(request):
    content = json.loads(request.body.decode("utf-8"))
    try:
        username, email, password = (
            content["username"],
            content["email"],
            content["password"],
        )
        if (
            User.objects.filter(email=email).exists()
            or User.objects.filter(username=username).exists()
        ):
            return HttpResponse(status=409)
        else:
            user = User(username=username, email=email, password=password)
            user.save()
            return HttpResponse(status=201)
    except:
        return HttpResponse(status=400)


@require_http_methods(["GET"])
def login(request):
    params = request.GET
    try:
        user = {
            "username/email": params["username/email"],
            "password": params["password"],
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(hours=1),
        }
        if (
            User.objects.filter(
                email=user["username/email"], password=user["password"]
            ).exists()
            or User.objects.filter(
                username=user["username/email"], password=user["password"]
            ).exists()
        ):
            token = jwt.encode(
                user,
                "login",
                algorithm="HS256",
            )
            return HttpResponse(status=200, content=token)
        else:
            return HttpResponse(status=401)
    except:
        return HttpResponse(status=400)
