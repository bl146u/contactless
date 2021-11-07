from django.urls import path

from apps.base import views


app_name = "base"

urlpatterns = [
    path("", views.ChatView.as_view(), name="chat"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
]
