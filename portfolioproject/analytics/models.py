from django.db import models

# Create your models here.
# mlapp/models.py
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
# mlapp/models.py
from django.db import models
from PIL import Image
from django.core.exceptions import ValidationError
from django.urls import reverse


class DataScienceProject(models.Model):
    """Model to represent a Data Science Project."""
    title = models.CharField(max_length=200, help_text="Title of the project")
    image = models.ImageField(upload_to='Datascience/')
    description = models.TextField(help_text="Brief description of the project")
    dataset_name = models.CharField(max_length=200, help_text="Name of the dataset used")
    popularity = models.PositiveIntegerField(default=0, help_text="Popularity of the project")
    dataset_description = models.TextField(help_text="Details about the dataset")
    dataset_source = models.URLField(blank=True, help_text="URL link to the dataset, if available")
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255)

    def clean(self):
        # Check if image size is more than 500 KB
        if self.image and self.image.size > 500 * 1024:
            raise ValidationError("Image file size should not exceed 500 KB")

    def get_absolute_url(self):
        """Return the absolute URL for this project."""
        return reverse('datascience_project_detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.title

    def increase_popularity(self):
        """Method to increase popularity by 1."""
        self.popularity += 1
        self.save()

    def decrease_popularity(self):
        """Method to decrease popularity by 1 (ensure it doesn’t go below 0)."""
        if self.popularity > 0:
            self.popularity -= 1
            self.save()


class EDA(models.Model):
    """Model to store Exploratory Data Analysis details for a project."""
    project = models.ForeignKey(DataScienceProject, on_delete=models.CASCADE, related_name='eda')
    title = models.TextField(help_text="Details of the EDA analysis", default='Null')
    analysis_type = models.CharField(
        max_length=50,
        choices=[
            ('univariate', 'Univariate'),
            ('bivariate', 'Bivariate'),
            ('multivariate', 'Multivariate'),
            ('others','others')
        ],
        help_text="Type of EDA analysis"
    )
    CHART_TYPES = [
        ('histogram', 'Histogram'),
        ('boxplot', 'Boxplot'),
        ('scatterplot', 'Scatter Plot'),
        ('barchart', 'Bar Chart'),
        ('countplot', 'Count Plot'),
        ('violinplot', 'Violin Plot'),
        ('heatmap', 'Heatmap'),
        ('pairplot', 'Pair Plot'),
        ('linechart', 'Line Chart'),
        ('piechart', 'Pie Chart'),
        ('kdeplot', 'KDE Plot'),
        ('swarmplot', 'Swarm Plot'),
        ('others', 'Others')
    ]
    col_size = models.CharField(
        max_length=50,
        choices=[
            ('col-4', 'col-4'),
            ('col-6', 'col-6'),
            ('col-8', 'col-8'),
            ('col-12', 'col-12')
        ],
        help_text="size of the column",blank=True,null=True
    )
    chart_type = models.CharField(
        max_length=50, choices=CHART_TYPES, help_text="Type of chart used in EDA",blank=True,null=True
    )
    popularity = models.PositiveIntegerField(default=0, help_text="Popularity of the project")
    img = models.ImageField(upload_to='EDA/')
    analysis_details = models.TextField(help_text="Details of the EDA analysis")
    insights = models.TextField(help_text="Insights derived from this EDA")

    def __str__(self):
        return f"{self.analysis_type.capitalize()} Analysis for {self.project.title}"

    def increase_popularity(self):
        """Method to increase popularity by 1."""
        self.popularity += 1
        self.save()

    def decrease_popularity(self):
        """Method to decrease popularity by 1 (ensure it doesn’t go below 0)."""
        if self.popularity > 0:
            self.popularity -= 1
            self.save()


class MLModel(models.Model):
    """Model to store Machine Learning model details."""
    project = models.ForeignKey(DataScienceProject, on_delete=models.CASCADE, related_name='ml_models')
    model_name = models.CharField(max_length=200, help_text="Name of the ML model used")
    popularity = models.PositiveIntegerField(default=0, help_text="Popularity of the project")
    img = models.ImageField(upload_to='ML/',blank=True)
    training_details = models.URLField(
        help_text="Add url of Prediction Url",
        null=True,
        blank=True
    )
    evaluation_metrics = models.TextField(help_text="Evaluation metrics for the model")
    insights = models.TextField(help_text="Key insights from the ML model")

    def increase_popularity(self):
        """Method to increase popularity by 1."""
        self.popularity += 1
        self.save()

    def decrease_popularity(self):
        """Method to decrease popularity by 1 (ensure it doesn’t go below 0)."""
        if self.popularity > 0:
            self.popularity -= 1
            self.save()

    def __str__(self):
        return f"{self.model_name} for {self.project.title}"
class DashboardMetric(models.Model):
    """Model to store dashboard metrics, such as new user statistics."""
    project = models.ForeignKey(DataScienceProject, on_delete=models.CASCADE, related_name='DashboardMetric')
    title = models.CharField(max_length=200, help_text="Title of the metric (e.g., 'New Users')")
    icon = models.CharField(max_length=200, help_text="Icon identifier for the metric (e.g., 'mingcute:user-follow-fill')")
    value = models.PositiveIntegerField(default=0, help_text="Numeric value of the metric (e.g., '15000')")
    description = models.CharField(max_length=500, blank=True, help_text="Short description of the metric (optional)")

    def __str__(self):
        return f"{self.title}: {self.value}"
