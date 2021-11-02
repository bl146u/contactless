from django.views.generic import TemplateView

from apps.base.mixins import AuthViewMixin


class FrontView(AuthViewMixin, TemplateView):
    template_name = "index.html"
