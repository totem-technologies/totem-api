import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase
from django.urls import reverse
from sesame.utils import get_query_string

from totem.circles.tests.factories import CircleEventFactory, CircleFactory
from totem.onboard.models import OnboardModel
from totem.users.models import User
from totem.users.tests.factories import UserFactory
from totem.users.views import user_detail_view, user_redirect_view

from ..views import user_index_view

pytestmark = pytest.mark.django_db


def test_user_update_view(client):
    user = UserFactory(verified=True)
    client.force_login(user)
    response = client.get(reverse("users:update"))
    assert response.status_code == 200
    response = client.post(reverse("users:update"), {"email": "new@example.com"})
    assert user.email != "new@example.com"
    assert response.status_code == 302
    assert response.url == reverse("users:dashboard")
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    user.refresh_from_db()
    assert user.email == "new@example.com"
    assert user.verified is False


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url")
        request.user = user
        response = user_redirect_view(request)
        assert response.status_code == 302
        assert response.url == reverse("onboard:index")
        OnboardModel.objects.create(user=user)
        user.onboard.onboarded = True
        response = user_redirect_view(request)
        assert response.status_code == 302
        assert response.url == reverse("users:dashboard")


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = user_detail_view(request, slug=user.slug)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        response = user_detail_view(request, slug=user.slug)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"


def test_user_index_view():
    factory = RequestFactory()
    request = factory.get("/someroute")
    request.user = AnonymousUser()
    response = user_index_view(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse("users:login") + "?next=/someroute"

    user = UserFactory()
    request.user = user
    response = user_index_view(request)
    assert response.status_code == 302
    assert response.url == "/onboard/"

    OnboardModel.objects.create(user=user)
    user.onboard.onboarded = True
    user.onboard.save()
    response = user_index_view(request)
    assert response.status_code == 302
    assert response.url == "/users/dashboard/"


def test_magic_login_view_verify_email(client):
    user = UserFactory()
    user.verified = False
    qs = get_query_string(user)
    response = client.get(reverse("magic-login") + qs)
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0
    user.refresh_from_db()
    assert user.verified is True

    qs = get_query_string(user)
    response = client.get(reverse("magic-login") + qs)
    assert response.status_code == 302
    assert len(get_messages(response)) == 0
    user.refresh_from_db()
    assert user.verified is True


class UserProfileImageViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_user_profile_image_view(self):
        url = reverse("users:profile-image")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/_profile_image_edit.html")

        # Test POST request
        data = {"randomize": True}
        oldseed = self.user.profile_avatar_seed
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/_profile_image_edit.html")
        self.user.refresh_from_db()
        assert oldseed != self.user.profile_avatar_seed


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = user = UserFactory()
        circle = CircleFactory(author=user)
        event = CircleEventFactory(circle=circle)
        event.attendees.add(user)
        event.joined.add(user)
        circle.subscribed.add(user)
        self.client.force_login(user)

    def test_user_profile_view(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["object"], self.user)
        self.assertEqual(len(response.context["subscribed_circles"]), 1)
        self.assertEqual(len(response.context["circle_history"]), 1)
        self.assertEqual(response.context["circle_count"], 1)
