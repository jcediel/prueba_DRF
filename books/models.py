from django.db import models


# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField(blank=True)
    isbn = models.BigIntegerField(unique=True)
    pages = models.IntegerField()

    def __str__(self):
        return self.title
