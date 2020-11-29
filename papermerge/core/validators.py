import re

from django.core.exceptions import ValidationError


def safe_character_validator(value):

    unsafe_chars = re.compile(r'.*[<>\/\\;:&].*')
    message = 'Enter only safe characters.'

    if unsafe_chars.match(value):
        raise ValidationError(message)
