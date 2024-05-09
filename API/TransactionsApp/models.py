from django.db import models
from taggit.managers import TaggableManager


class Transaction(models.Model):
    owner_id = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField()
    is_expense = models.BooleanField(default=False)
    category_id = models.ForeignKey('Category', null=True, related_name='transactions', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    user_tags = TaggableManager(blank=True)


    def __str__(self):
        return f'Owner: {self.owner_id}, \
            Amount: {self.amount}, \
            Date: {self.date}, \
            Is expense: {self.is_expense}, \
            Category: {self.category_id}, \
            Description: {self.description}, \
            Tags: {self.user_tags}'
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'Name: {self.name}, \
            Description: {self.description}'
