from django.urls import reverse
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect

from apps.base.mixins import AuthViewMixin


class ChatView(AuthViewMixin, TemplateView):
    template_name = "chat.html"


class SignUpView(TemplateView):
    template_name = "sign-up.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("base:chat"))
        return super().dispatch(request, *args, **kwargs)
