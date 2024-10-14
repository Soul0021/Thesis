from django.db import models
from django.urls import reverse
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
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    is_quiz = models.BooleanField(default=False)
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Assuming 'quiz_view' is the correct URL name
        return reverse('userauths:quiz1', kwargs={'step': self.order})




# Model for tracking user progress across different levels and roadmap steps
class UserProgress(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),  # User has started but not finished
        ('locked', 'Locked'),  # User can't access this step yet
        ('unlocked', 'Unlocked'),  # User can access this step
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    roadmap_step = models.ForeignKey(RoadmapStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='locked')  # Default to locked

    def __str__(self):
        return f'{self.user.username} - {self.level.name} - {self.roadmap_step.name}'

    class Meta:
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progresses'
        unique_together = ('user', 'level', 'roadmap_step')  # Ensure uniqueness for user-level-roadmap_step

class Vowel(models.Model):
    symbol = models.CharField(max_length=10)
    sound = models.CharField(max_length=50)

    def __str__(self):
        return self.symbol