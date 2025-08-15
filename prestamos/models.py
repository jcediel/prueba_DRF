from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from books.models import Books
from decimal import Decimal


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


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"

    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, related_name="books_reservated"
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="members_reservated"
    )
    status = models.CharField(
        choices=Status.choices, max_length=10, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.book}"


class Penalty(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        CANCELLED = "CANCELLED", "Cancelled"

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    rate_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    days_late = models.IntegerField()
    amount_cached = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.loan} - {self.status}"

    def calc_amount(self):
        total = (Decimal(self.days_late) * self.rate_per_day).quantize(Decimal("0.01"))
        self.amount_cached = total
        return total


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    external_ref = models.CharField(max_length=20, unique=True)
    penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member} - {self.amount}"
