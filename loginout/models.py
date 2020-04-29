from django.db import models


# Create your models here.

class UserDetails(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    country_code = models.CharField(max_length=2, null=True)
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username + ' ' + self.email + ' ' + str(self.id)

