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

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        constraints = [
            # Case-insensitive unique title
            UniqueConstraint(
                Lower('title'),
                name='title_unique',
            ),
        ]
