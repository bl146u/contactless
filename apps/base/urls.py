from django.urls import path

from apps.base import views


app_name = "base"

urlpatterns = [
    path("", views.FrontView.as_view(), name="front"),
]
