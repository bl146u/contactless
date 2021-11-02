from django.urls import path

from apps.ws import consumers


app_name = "ws"


urlpatterns = [
    path("sign-in/", consumers.SignInConsumer.as_asgi(), name="sign-in"),
    path("", consumers.MainConsumer.as_asgi(), name="main"),
]
