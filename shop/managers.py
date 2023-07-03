from django.db import models
from datetime import datetime, timedelta
from django.db.models import Q, Sum


class ActiveShopManager(models.Manager):
    """
    Active Shops manager.
    """

    def get_queryset(self):
        return super(ActiveShopManager, self).get_queryset().filter(status='a')


class ShopInvoiceManager(models.Manager):
    def get_weekly_records(self, shop):
        one_week_ago = datetime.now() - timedelta(days=7)
        conditions = Q()
        records = []
        for i in range(8):
            day = one_week_ago + timedelta(days=i)
            conditions |= Q(created__date=day.date(), invoice_shop='sales', shop=shop)
            # query = self.select_related(None).filter(conditions)
            # records.append((i, sum(record.get_total_invoice_price() for record in query)))

        return sum(record.get_total_invoice_price() for record in self.filter(conditions))
