from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from books.models import Books


# Create your models here.
class Member(AbstractUser):
    ROLE_CHOICES = (
        ("staff", "Staff"),
        ("basic", "Basic"),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10)

    def __str__(self):
        return f"{self.name} - {self.role}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name", "role"]


class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="members")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="books")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.member} - {self.book}"
