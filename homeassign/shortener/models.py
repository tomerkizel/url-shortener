from django.db import models
from django.db.models import F
from django.db import transaction


class UrlRedirect(models.Model):
    original_url = models.CharField(max_length=200)
    # unique=True allows us to avoid any generated url duplications
    generated_redirect = models.CharField(max_length=200, unique=True) 
    count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.original_url
