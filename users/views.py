from typing import Any
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .forms import CustomSignUpForm


@method_decorator(csrf_exempt, name="dispatch")
class SignUpView(CreateView):
    """
    View for user sign up page.

    Attributes:
    form_class (CustomSignUpForm): The form used for user sign up.
    template_name (str): The name of the template used for rendering the sign up page.
    """

    form_class = CustomSignUpForm
    template_name = "users/signup.html"

    def form_valid(self, form):
        """
        Method called when the form is valid.

        Args:
        form (CustomSignUpForm): The form instance with the validated data.

        Returns:
        HttpResponse: The HTTP response with the success message.
        """
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "You have successfully signed up!")
        return response

    def form_invalid(self, form):
        """
        Method called when the form is invalid.

        Args:
        form (CustomSignUpForm): The form instance with the invalid data.

        Returns:
        HttpResponse: The HTTP response with the error message.
        """
        response = super().form_invalid(form)
        messages.error(
            self.request, "There was an error with your submission. Please try again."
        )
        return response

    def get_success_url(self):
        """
        Method called to get the URL to redirect to after a successful form submission.

        Returns:
        str: The URL to redirect to.
        """
        return reverse_lazy("posts:home")


class CustomLogin(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("posts:home")


class CustomLogout(LogoutView):
    pass


class UserProfile(DetailView):
    """
    A view that displays a user's profile page, including their posts.

    If a user's primary key (pk) is provided in the URL, the view will display
    the profile page for that user. Otherwise, it will display the profile page
    for the currently logged-in user.

    The context data for this view includes the user object and a queryset of
    all posts associated with the user.
    """

    model = get_user_model()
    template_name = "users/profile.html"

    def get_object(self):
        if self.kwargs.get("pk"):
            return get_object_or_404(get_user_model(), pk=self.kwargs["pk"])
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        context["posts"] = context["user"].post_set.all()
        return context


class UpdateProfile(UpdateView):
    model = get_user_model()
    template_name = "users/update_profile.html"
    fields = ["first_name", "last_name", "email", "avatar"]

    def get_object(self):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse_lazy("users:user-profile", kwargs={"pk": self.object.pk})


class DeleteProfile(DeleteView):
    model = get_user_model()
    template_name = "posts/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("posts:home")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["obj"] = f"User: {self.object}"
        return context

    def get_object(self, queryset=None) -> Any:
        return self.request.user
