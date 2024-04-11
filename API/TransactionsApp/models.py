from django.db import models
from taggit.managers import TaggableManager


class Transaction(models.Model):
    ownerId = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=100)
    amount = models.IntegerField()
    tags = TaggableManager()

    def __str__(self):
        return f'Owner: {self.ownerId}, \
            Date: {self.date}, \
            Type: {self.type}, \
            Amount: {self.amount}'