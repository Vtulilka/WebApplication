from django.db import models

# Create your models here.

class Budjet(models.Model):
    owner_id = models.ForeignKey('auth.User', related_name='budjets', on_delete=models.CASCADE)
    amount = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=50)


    def __str__(self):
        return f'Name: {self.name}, \
                Owner: {self.owner_id}, \
                Amount: {self.amount}, \
                Start: {self.start_date}, \
                End: {self.end_date}'