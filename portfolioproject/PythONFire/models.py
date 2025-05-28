from django.db import models

# Create your models here.
from django.db import models

class PythonProject(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    name = models.CharField(max_length=255)
    popularity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )
    def __str__(self):
        return self.name
