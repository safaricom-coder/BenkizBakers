from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

# Consolas,Lucida Console,Lucida,Lucida Sans Typewriter,Cascadia Code

from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Payment Info
    customerName = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Lipia identifiers
    transaction_reference = models.CharField(max_length=255, unique=True, null=True, blank=True)
    merchantRequestID = models.CharField(max_length=255, blank=True, null=True)
    external_reference = models.CharField(max_length=255, blank=True, null=True)

    # Mpesa receipt
    mpesaReceiptNumber = models.CharField(max_length=50, blank=True, null=True)

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    status_bool = models.BooleanField(default=False)

    # API response data
    responseCode = models.CharField(max_length=10, blank=True, null=True)
    responseDescription = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status_feedback = models.CharField(max_length=150, blank=True, null=True)

    # Full raw callback storage
    callback_body = models.TextField(blank=True, null=True)

    # Timestamps
    transaction_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_reference or 'NoRef'} - {self.status}"