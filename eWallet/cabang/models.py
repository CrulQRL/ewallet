from django.db import models

class Customer(models.Model):
    user_id = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200, null=True)
    saldo = models.IntegerField(default=0)
    ip = models.CharField(max_length=100, default='')
    is_domisili = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id + ' - ' + self.nama