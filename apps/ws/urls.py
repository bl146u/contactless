from django.urls import path

from apps.ws import consumers


app_name = "ws"


urlpatterns = [
    path("sign-in/", consumers.SignInConsumer.as_asgi(), name="sign-in"),
    path("sign-out/", consumers.SignOutConsumer.as_asgi(), name="sign-out"),
    path("sign-up/", consumers.SignUpConsumer.as_asgi(), name="sign-up"),
    path("send/", consumers.SendConsumer.as_asgi(), name="send"),
    path("files/", consumers.FilesConsumer.as_asgi(), name="files"),
]
