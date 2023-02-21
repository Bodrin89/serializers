
from django.db import models
from django.db.models import CASCADE

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images', null=False)
    is_published = models.BooleanField()
    author = models.ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name
