from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator


validate_username = UnicodeUsernameValidator()
validate_password = validate_password