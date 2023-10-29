from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomSignUpForm(UserCreationForm):
    """
    Form for signing up a new user.

    Inherits from Django's built-in UserCreationForm class and provides fields for email, first name, and last name.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "first_name", "last_name"]
