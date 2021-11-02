from django.views.generic import TemplateView


class AuthViewMixin(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = "denied.html"
        return super().dispatch(request, *args, **kwargs)
