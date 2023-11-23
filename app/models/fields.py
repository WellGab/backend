import uuid
import re


class ValidationError(Exception):
    pass


class BaseField:
    def __init__(self, **kwargs):
        self.required = kwargs.get('required', False)
        self.default = kwargs.get('default', None)
        self.unique = kwargs.get('unique', False)

    def validate(self, value):
        pass


class StringField(BaseField):
    def validate(self, value):
        super().validate(value)
        if not isinstance(value, str):
            raise ValidationError("Field must be a string")


class EmailField(StringField):
    def validate(self, value):
        super().validate(value)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Invalid email address")


class UUIDField(StringField):
    def validate(self, value):
        super().validate(value)
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValidationError("Invalid UUID")
