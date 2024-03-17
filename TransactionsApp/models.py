from django.db import models

# Create your models here.
class Transaction(models.Model):
    ownerId = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=100)
    amount = models.IntegerField()

    def __str__(self):
        return f'Owner: {self.OwnerId}, \
            Date: {self.Date}, \
            Type: {self.Type}, \
            Amount: {self.amount}'