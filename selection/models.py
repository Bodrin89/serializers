from django.db import models
from django.db.models import CASCADE

from ads.models import Ad
from users.models import User


class Selection(models.Model):

    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Ad)
    owner = models.ForeignKey(User, on_delete=CASCADE)
