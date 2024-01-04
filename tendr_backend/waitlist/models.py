from django.db import models

from tendr_backend.common.models import Common

class Waiter(Common):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 16, blank=True, null=True)
    other = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name
