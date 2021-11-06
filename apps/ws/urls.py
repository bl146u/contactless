from django.urls import path

from apps.ws import consumers


app_name = "ws"


urlpatterns = [
    path("sign-in/", consumers.SignInConsumer.as_asgi(), name="sign-in"),
    path("sign-out/", consumers.SignOutConsumer.as_asgi(), name="sign-out"),
    path("send/", consumers.SendConsumer.as_asgi(), name="send"),
]
