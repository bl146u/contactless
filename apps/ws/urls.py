from django.urls import path

from apps.ws import views


app_name = "ws"


urlpatterns = [
    path("", views.websocket_view, name="main"),
]
