from django.http import Http404


class CustomerProjectAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user in self.get_object().customers.all() or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class CustomerInvoiceAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user in self.get_object().project.customers.all() or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        raise Http404
