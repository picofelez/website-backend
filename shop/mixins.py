from django.http import Http404


class ShopPanelAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_object() in request.user.shops.all():
            return super().dispatch(request, *args, **kwargs)
        raise Http404
