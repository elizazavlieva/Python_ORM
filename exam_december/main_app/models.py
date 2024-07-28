from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.choices import SurfaceTypeChoices
from main_app.managers import TennisPlayerManager


# Create your models here.


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5)
        ]
    )
    birth_date = models.DateField()

    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )
    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    is_active = models.BooleanField(
        default=True,
    )
    objects = TennisPlayerManager()

    def __str__(self):
        return self.full_name


class Tournament(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(2)
        ]
    )
    location = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    start_date = models.DateField()

    surface_type = models.CharField(
        max_length=12,
        choices=SurfaceTypeChoices.choices,
        default='Not Selected',
    )


class Match(models.Model):
    score = models.CharField(
        max_length=100,
    )
    summary = models.TextField(
        validators=[
            MinLengthValidator(5)
        ]
    )
    date_played = models.DateTimeField()

    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name='tournaments'
    )

    players = models.ManyToManyField(
        to=TennisPlayer,
        related_name='players'
    )
    winner = models.ForeignKey(
        to=TennisPlayer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='winner'
    )

    class Meta:
        verbose_name_plural = 'Matches'
