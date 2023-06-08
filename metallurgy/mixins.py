from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse


class CustomerProjectAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user in self.get_object().customers.all() or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        return redirect(
            f"{reverse('account:otp-login')}?next={reverse('metallurgy:customer-project-detail', args=[self.get_object().id])}"
        )


class CustomerInvoiceAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user in self.get_object().project.customers.all() or request.user.is_superuser
        ):
            return super().dispatch(request, *args, **kwargs)
        return redirect(
            f"{reverse('account:otp-login')}?next={reverse('metallurgy:customer-invoice-detail', args=[self.get_object().id])}"
        )
