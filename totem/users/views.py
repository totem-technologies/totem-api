from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, FormView, RedirectView, UpdateView
from sesame.utils import get_query_string

from totem.email.utils import send_mail

from .forms import LoginForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class LogInView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("users:login")

    def _message(self):
        messages.success(self.request, "Check your email for a login link.")

    def form_valid(self, form):
        success_url = form.cleaned_data.get("success_url")
        if success_url:
            self.success_url = success_url
        else:
            # Always set message no matter what
            self._message()

        email = form.cleaned_data["email"].lower()

        existing = False

        try:
            user = User.objects.get(email=email)
            existing = True
        except User.DoesNotExist:
            user = User.objects.create(email=email)

        url = self.request.build_absolute_uri(reverse("magic-login")) + get_query_string(user)
        url += "&next=" + form.cleaned_data.get("after_login_url", reverse("pages:home"))
        if existing:
            self.email_returning_user(user, url)
        else:
            self.email_new_user(user, url)
        return super().form_valid(form)

    def email_returning_user(self, user, url):
        send_mail(
            "Login to ✨Totem✨",
            "old_login",
            {"url": mark_safe(url)},
            recipient_list=[user.email],  # type: ignore
        )

    def email_new_user(self, user, url):
        send_mail(
            "Welcome to ✨Totem✨",
            "new_login",
            {"url": mark_safe(url)},
            recipient_list=[user.email],  # type: ignore
        )
