from django.urls import path

from apps.api import views


app_name = "api_v1"

urlpatterns = [
    path("config/", views.ConfigAPIView.as_view(), name="config"),
]
