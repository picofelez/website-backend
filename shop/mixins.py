from django.http import Http404
from django.shortcuts import get_object_or_404

from shop.models import Shop


class ShopPanelAccessMixin:
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, *kwargs)
    #     self.shop = get_object_or_404(Shop, unique_uuid=self.kwargs.get('unique_uuid'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['shop'] = self.shop
        return context

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(Shop, unique_uuid=self.kwargs.get('unique_uuid'))
        if request.user.is_authenticated and self.shop in request.user.shops.all():
            return super().dispatch(request, *args, **kwargs)
        raise Http404
