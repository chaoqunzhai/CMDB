from django.db import models

# Create your models here.

class cmdbadmin(models.Model):
    name = models.CharField(max_length=32)


    class Meta:
        verbose_name_plural = 'CMDBadmin'