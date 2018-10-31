# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Credentials(models.Model):
    servername = models.CharField(max_length=100)
    port = models.IntegerField()
    cloud = models.CharField(max_length=50)
    uuid = models.UUIDField()
    token = models.CharField(max_length=32)

