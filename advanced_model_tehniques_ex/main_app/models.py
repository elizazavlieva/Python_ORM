from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator
from django.db import models

from main_app.mixin import RechargeEnergyMixin
from main_app.validators import name_validator


# Create your models here.


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            name_validator
        ]
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message='Age must be greater than or equal to 18')
        ]
    )
    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits")
        ]
    )
    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )


class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    genre = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

class BaseMedia(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created_at", "title"]

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    genre = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"

    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, "Author must be at least 5 characters long"),
        ]
    )

    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, "ISBN must be at least 6 characters long"),
        ]
    )


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"

    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, "Director must be at least 8 characters long"),
        ]
    )


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"

    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, "Artist must be at least 9 characters long"),
        ]
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self):
        tax = Decimal(0.08)
        return self.price * tax

    def calculate_shipping_cost(self, weight: Decimal):
        multiplier = Decimal(2.0)
        return weight * multiplier

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        discount = Decimal(1.2)
        return self.price * discount

    def calculate_tax(self):
        tax = Decimal(0.05)
        return self.price * tax

    def calculate_shipping_cost(self, weight: Decimal):
        multiplier = Decimal(1.5)
        return weight * multiplier

    def format_product_name(self):
        return f"Discounted Product: {self.name}"

class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(
        max_length=100,
    )

    hero_title = models.CharField(
        max_length=100,
    )

    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self):
        if self.energy - 80 >= 0:
            self.energy -= 80 if self.energy - 80 > 0 else 79
            self.save()
            return f"{self.name} as Spider Hero swings from buildings using web shooters"

        return f"{self.name} as Spider Hero is out of web shooter fluid"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self):
        if self.energy - 65 >= 0:
            self.energy -= 65 if self.energy - 65 > 0 else 64
            self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

        return f"{self.name} as Flash Hero needs to recharge the speed force"


class Document(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["search_vector"])
        ]

    title = models.CharField(
        max_length=200,
    )

    content = models.TextField()

    search_vector = SearchVectorField(
        null=True,
    )