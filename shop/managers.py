from django.db import models
from datetime import datetime, timedelta
from django.db.models import Q, Sum, Count
from django.db.models.functions import ExtractDay

from extensions.utils import jalali_converter


class ActiveShopManager(models.Manager):
    """
    Active Shops manager.
    """

    def get_queryset(self):
        return super(ActiveShopManager, self).get_queryset().filter(status='a')


class ShopInvoiceManager(models.Manager):
    def get_weekly_records(self, shop):
        one_week_ago = datetime.now() - timedelta(days=7)
        records = []
        days = []
        for i in range(8):
            day = one_week_ago + timedelta(days=i)
            days.append(jalali_converter(day.date()))

            qs = self.select_related(None).filter(
                created__year=day.year,
                created__month=day.month,
                created__day=day.day,
                invoice_shop='sales',
                shop=shop
            ).annotate(
                day=ExtractDay('created'),
            ).order_by('day')
            records.append(sum(record.get_total_invoice_price() for record in qs))

        return [days, records]
