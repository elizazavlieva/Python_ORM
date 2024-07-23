from django.core.exceptions import ValidationError


class RangeValueValidator:
    def __init__(self, min_range, max_range, message=None):
        self.min_range = min_range
        self.max_range = max_range
        self.message = message


    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"The rating must be between {self.min_range:.1f} and {self.max_range:.1f}"
        else:
            self.__message = value

    def __call__(self, value:int):
        if not self.min_range <= value <= self.max_range:
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            'main_app.validators.ValueValidator',
            [self.min_range, self.max_range],
            {'message': self.message},
        )