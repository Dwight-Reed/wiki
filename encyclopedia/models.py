from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    pass


class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    history = HistoricalRecords()

    class Meta:
        ordering = ["title"]

        constraints = [
            # Case-insensitive unique title
            UniqueConstraint(
                Lower("title"),
                name="title_unique",
            ),
        ]


class Image(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="images/")
    history = HistoricalRecords()
