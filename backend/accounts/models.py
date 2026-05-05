from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    warehouse = models.ForeignKey(
        'inventory.Warehouse', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='staff'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
