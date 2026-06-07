from django.db import models
from django.contrib.auth.models import User


# ---------------------------
# USER PROFILE MODEL
# ---------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)

    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username


# ---------------------------
# NGO MODEL
# ---------------------------
class NGO(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()

    achievements = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)

    # NEW FIELD
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"