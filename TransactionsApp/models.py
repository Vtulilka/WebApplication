from django.db import models

# Create your models here.
class Transaction(models.Model):
    OwnerId = models.ForeignKey('auth.User', related_name='transactions', on_delete=models.CASCADE)
    transactionDate = models.DateTimeField()
    transactionType = models.CharField(max_length=100)
    amount = models.IntegerField()

    def __str__(self):
        return f'Owner: {self.transactionOwnerId}, \
            Date: {self.transactionDate}, \
            Type: {self.transactionType}, \
            Amount: {self.amount}'