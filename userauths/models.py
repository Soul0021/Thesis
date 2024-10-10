from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

# Model for different learning levels
class Level(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'


# Model for steps in the roadmap
class RoadmapStep(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)  # ForeignKey to Level

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Roadmap Step'
        verbose_name_plural = 'Roadmap Steps'


# Model for tracking user progress across different levels and roadmap steps
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    roadmap_step = models.ForeignKey(RoadmapStep, on_delete=models.CASCADE)
    progress = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('locked', 'Locked')])

    def __str__(self):
        return f'{self.user.username} - {self.level.name} - {self.roadmap_step.name}'

    class Meta:
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progresses'
        unique_together = ('user', 'level', 'roadmap_step')  # Ensures uniqueness of user-level-roadmap_step combination
