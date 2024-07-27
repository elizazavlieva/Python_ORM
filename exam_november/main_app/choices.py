from django.db import models



class CategoryChoices(models.TextChoices):
    TECHNOLOGY = 'Technology', 'Technology'
    SCIENCE = 'Science', 'Science'
    EDUCATION = 'Education', 'Education'
