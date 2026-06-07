from django.db import models
from django.contrib.auth.models import User


# ---------------- ACTIVITY ----------------
class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    date = models.DateField()
    location = models.CharField(max_length=200)

    seats = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Open', 'Open'),
            ('Closed', 'Closed'),
            ('Completed', 'Completed')
        ],
        default='Open'
    )

    coordinators = models.ManyToManyField(
        User,
        related_name="coordinated_activities",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ useful for sorting

    def __str__(self):
        return self.title


# ---------------- ENROLLMENT ----------------
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    enrolled_at = models.DateTimeField(auto_now_add=True)

    # ✅ prevent duplicate enrollment
    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user.username} -> {self.activity.title}"