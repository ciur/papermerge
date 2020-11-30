import re

from django.core.exceptions import ValidationError


def safe_character_validator(value):
    """
    Unsafe characters are

    <  (smaller then)
    >  (greater then)
    \\  (backslash)
    /  (slash)

    & and ; may be added by escape:

    <script>alert('hi!')</script> after escaping becomes:

    &lt;script&gt;alert(&#x27;hi!&#x27;)&lt;/script&gt;
    """
    unsafe_chars = re.compile(r'.*[<>\/\\:].*')
    message = 'Enter only safe characters.'

    if unsafe_chars.match(value):
        raise ValidationError(message)
