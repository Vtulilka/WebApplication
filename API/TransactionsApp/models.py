from django.db import models
from taggit.managers import TaggableManager


class Transaction(models.Model):
    owner_id = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField()
    type = models.CharField(max_length=20)
    category_id = models.ForeignKey('Category', null=True, related_name='transactions', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    user_tags = TaggableManager(blank=True)


    def __str__(self):
        return f'Owner: {self.owner_id}, \
            Amount: {self.amount}, \
            Date: {self.date}, \
            Type: {self.type}, \
            Category: {self.category}, \
            Description: {self.description}, \
            Tags: {self.tags}'
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'Name: {self.name}, \
            Description: {self.description}'
