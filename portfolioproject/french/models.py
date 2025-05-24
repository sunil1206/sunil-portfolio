from PIL import Image
from django.db import models

# Create your models here.
from django.db import models

class AboutMe(models.Model):
    title= models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='about/',null=True)
    birthday = models.DateField()
    degree = models.CharField(max_length=100)
    experience = models.IntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    freelance_available = models.BooleanField(default=False)
    bio = models.TextField()
    cv = models.FileField(upload_to='cv/', null=True, blank=True)  # Add this line
    video_profile = models.URLField(max_length=255, blank=True, null=True)  # Add this line
    github = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the uploaded image file
        img = Image.open(self.img.path)

        # Set the desired size
        target_size = (600, 600)

        # Resize the image to the target size
        img = img.resize(target_size, Image.LANCZOS)

        # Save the resized image back to the same path
        img.save(self.img.path)



class Qualification(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    date_range = models.CharField(max_length=20)
    description = models.TextField()
    order_number = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date_range = models.CharField(max_length=20)
    description = models.TextField()
    order_number = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.position} at {self.company}"


class Skill(models.Model):
    COLOR_CHOICES = [
        ('bg-primary', 'Primary'),
        ('bg-secondary', 'Secondary'),
        ('bg-success', 'Success'),
        ('bg-danger', 'Danger'),
        ('bg-warning', 'Warning'),
        ('bg-info', 'Info'),
        ('bg-dark', 'Dark'),
    ]

    name = models.CharField(max_length=50)
    percentage = models.IntegerField()
    progress_bar_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='bg-primary')

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=255)
    icon_class = models.CharField(max_length=50,default="fa-laptop")
    description = models.TextField()

    def __str__(self):
        return self.title

# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#
#     def __str__(self):
#         return self.subject