from django.core.exceptions import ValidationError


def validate_content(value):
    content = value
    if content == "":
        raise ValidationError("Content cannot be blank --> that will be changed in the future!")
    return value