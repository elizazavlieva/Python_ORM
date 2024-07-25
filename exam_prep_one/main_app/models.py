from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import GenreChoices
from main_app.manager import DirectorManager


# Create your models here.
class BaseModel(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    birth_date = models.DateField(
        default='1900-01-01',
    )
    nationality = models.CharField(
        max_length=50,
        default='Unknown',
    )

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True

class Director(BaseModel):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ],
    )

    objects = DirectorManager()


class Actor(BaseModel):

    is_awarded = models.BooleanField(
        default=False,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )


class Movie(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ]
    )
    release_date = models.DateField(
    )
    storyline = models.TextField(
        null=True,
        blank=True,

    )
    genre = models.CharField(
        max_length=6,
        choices=GenreChoices,
        default='Other',
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ],
        default=0.0,
    )
    is_classic = models.BooleanField(
        default=False,
    )
    is_awarded = models.BooleanField(
        default=False
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='director_movies'
    )
    starring_actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        related_name='starring_movies',
        blank=True,
        null=True,
    )
    actors = models.ManyToManyField(
        Actor,
        related_name='actor_movies'
    )