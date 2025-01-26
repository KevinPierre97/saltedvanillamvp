from django.core.exceptions import ValidationError
from profanityfilter import ProfanityFilter


def validate_profanity(value):
    pf = ProfanityFilter()
    if pf.is_profane(value):
        raise ValidationError("This field contains profanity")
