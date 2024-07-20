from django.core.exceptions import ValidationError
from django.db import models


def name_validator(value):
    for char in value:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError("Name can only contain letters and spaces")



