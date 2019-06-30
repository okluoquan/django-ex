# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Trade(models.Model):
    instrument_id = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    price = models.CharField(max_length=20)
    qty = models.CharField(max_length=20)
    trade_id = models.CharField(max_length=20, unique = True)
    side = models.CharField(max_length=1)
