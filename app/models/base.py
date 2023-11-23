import inflect
from .fields import BaseField
from ..utils import db_helpers, setup


class BaseModel(db_helpers.MongoDBActions):
    def __init__(self, **kwargs):
        for field_name, field in vars(self.__class__).items():
            if isinstance(field, BaseField):
                setattr(self, field_name, kwargs.get(
                    field_name, field.default))
                # Validate each field as it is set
                self.validate_field(field_name)

        # Validate all fields after initialization
        self.validate()

        super().__init__(self.get_model_name(), setup.db)

    def validate_field(self, field_name):
        field = getattr(self.__class__, field_name)
        value = getattr(self, field_name, None)

        if field.required and value is None:
            raise ValidationError(f"{field_name} is required")

        if value is not None:
            field.validate(value)

    def validate(self):
        for field_name, field in vars(self.__class__).items():
            if isinstance(field, BaseField):
                self.validate_field(field_name)

    def get_model_name(self):
        # Get the class name in snake_case
        class_name = self.__class__.__name__
        snake_case_name = ''.join(
            ['_' + c.lower() if c.isupper() else c for c in class_name]).lstrip('_')

        # Use inflect library to get the plural form
        pluralizer = inflect.engine()
        plural_name = pluralizer.plural_noun(snake_case_name)

        return plural_name


class ValidationError(Exception):
    pass
