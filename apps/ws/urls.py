from django.urls import path

from apps.ws import consumers


app_name = "ws"


urlpatterns = [
    path("", consumers.MainConsumer.as_asgi(), name="main"),
]
