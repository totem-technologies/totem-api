from __future__ import annotations

import urllib.parse
from datetime import datetime
from typing import TYPE_CHECKING

from django.conf import settings
from django.urls import reverse

if TYPE_CHECKING:
    from totem.circles.models import CircleEvent
    from totem.users.models import User

import mrml
from django.template.loader import render_to_string
from pydantic import AnyHttpUrl, BaseModel, TypeAdapter

from totem.utils.pool import global_pool

from .models import EmailLog
from .utils import send_brevo_email, send_mail


def type_url(url: str):
    return TypeAdapter(AnyHttpUrl).validate_python(url)


def _make_email_url(link) -> AnyHttpUrl:
    return type_url(urllib.parse.urljoin(settings.SITE_BASE_URL, link))


def _to_human_time(user: User, dt: datetime):
    # 06:56 PM EDT on Friday, August 25
    return dt.astimezone(user.timezone).strftime("%I:%M %p %Z on %A, %B %d")


class Email(BaseModel):
    template: str
    subject: str
    recipient: str
    support_email: str = settings.EMAIL_SUPPORT_ADDRESS
    show_env_banner: bool = settings.EMAIL_SHOW_ENV_BANNER
    environment: str = settings.ENVIRONMENT_NAME

    def render_html(self) -> str:
        s = render_to_string(f"email/emails/{self.template}.mjml", context=self.model_dump())
        return mrml.to_html(s)

    def render_text(self) -> str:
        return render_to_string(f"email/emails/{self.template}.txt", context=self.model_dump())

    def send(self, blocking: bool = True):
        if blocking:
            send_mail(
                subject=self.subject,
                html_message=self.render_html(),
                text_message=self.render_text(),
                recipient_list=[self.recipient],
            )
        else:
            global_pool.add_task(
                send_mail,
                subject=self.subject,
                html_message=self.render_html(),
                text_message=self.render_text(),
                recipient_list=[self.recipient],
            )
        EmailLog.objects.create(
            subject=self.subject,
            template=self.template,
            context=self.model_dump(mode="json"),
            recipient=self.recipient,
        )


class BrevoEmail(BaseModel):
    template_id: int
    recipient: str
    show_env_banner: bool = settings.EMAIL_SHOW_ENV_BANNER
    environment: str = settings.ENVIRONMENT_NAME

    def send(self):
        send_brevo_email(
            template_id=self.template_id,
            recipient=self.recipient,
        )


class WelcomeEmail(BrevoEmail):
    template_id: int = 3


class ButtonEmail(Email):
    template: str = "button"
    button_text: str
    link: AnyHttpUrl
    title: str
    message: str


class LoginEmail(ButtonEmail):
    button_text: str = "Sign in"
    subject: str = "Totem sign in link"
    title: str = "Sign in link"
    message: str = "You requested a link to sign in, and here it is! Note that this link expires in an hour and can only be used once."


class ChangeEmailEmail(ButtonEmail):
    link: AnyHttpUrl
    button_text: str = "Confirm"
    subject: str = "Confirm your new email address"
    title: str = "Confirm your new email address"
    message: str = "You're almost there! Please confirm your new email address by clicking the button below."


class CircleStartingEmail(Email):
    template: str = "circle_starting"
    start: str
    event_title: str
    event_link: AnyHttpUrl
    link: AnyHttpUrl
    button_text: str = "Join Session"
    subject: str = "Your Space is starting soon"
    title: str = "Get Ready"


class CircleAdvertisementEmail(Email):
    template: str = "circle_ad"
    start: str
    event_title: str
    space_title: str
    space_subtitle: str
    author: str
    unsubscribe_url: AnyHttpUrl
    link: AnyHttpUrl
    button_text: str = "Reserve a spot"
    subject: str = "New Session"
    event_details: str | None
    title: str
    subtitle: str
    image_url: str | None
    author_image_url: str | None


class CircleTomorrowReminderEmail(Email):
    template: str = "circle_tomorrow_reminder"
    start: str
    event_title: str
    link: AnyHttpUrl
    button_text: str = "Add to calendar"
    subject: str = "You have a session coming up tomorrow"
    title: str = "Space Tomorrow"


class CircleSignupEmail(Email):
    template: str = "circle_signup"
    start: str
    event_title: str
    link: AnyHttpUrl
    button_text: str = "Add to calendar"
    subject: str = "Your spot is saved"
    title: str = "Spot Saved"


class TestEmail(Email):
    template: str = "test"
    start: str
    event_title: str
    link: AnyHttpUrl
    button_text: str = "Add to calendar"
    subject: str = "Your spot is saved"
    title: str = "Spot Saved"


class MissedEventEmail(Email):
    template: str = "missed_event"
    start: str
    event_title: str
    link: AnyHttpUrl = type_url("https://forms.gle/qnEKej6Pt4JAZTH79")
    event_link: AnyHttpUrl
    button_text: str = "Let us know how we can help"
    subject: str = "We missed you!"
    title: str = "We missed you!"


def send_welcome_email(user: User):
    WelcomeEmail(recipient=user.email).send()
    if settings.DEBUG:
        print("------------------------------------------")
        print(f"Sending welcome email to {user.email}")
        print("------------------------------------------")


def send_returning_login_email(email: str, url: str):
    _url = _make_email_url(url)
    LoginEmail(
        recipient=email,
        link=_url,
    ).send()

    if settings.DEBUG:
        print("------------------------------------------")
        print(f"Sending email to {email} with link\n{_url}")
        print("------------------------------------------")


def send_change_email(old_email: str, new_email: str, login_url: str):
    ChangeEmailEmail(
        recipient=new_email,
        link=_make_email_url(login_url),
    ).send()


def send_notify_circle_starting(event: CircleEvent, user: User):
    start = _to_human_time(user, event.start)
    CircleStartingEmail(
        recipient=user.email,
        start=start,
        event_title=event.circle.title,
        event_link=_make_email_url(event.get_absolute_url()),
        link=type_url(event.join_url(user)),
    ).send()


def send_notify_circle_tomorrow(event: CircleEvent, user: User):
    start = _to_human_time(user, event.start)
    title = event.title or event.circle.title or event.circle.title
    CircleTomorrowReminderEmail(
        title=f"Tomorrow: {title}",
        subject=f"Tomorrow: {title}",
        recipient=user.email,
        start=start,
        event_title=event.circle.title,
        link=_make_email_url(event.get_absolute_url()),
    ).send()


def send_notify_circle_advertisement(event: CircleEvent, user: User):
    start = _to_human_time(user, event.start)
    title = event.title or event.circle.subtitle
    subtitle = event.circle.title
    details = None
    if event.content:
        details = event.content_html
    elif event.circle.content:
        details = event.circle.content_html
    image_url = event.circle.image.url if event.circle.image else None
    author_image_url = event.circle.author.profile_image.url if event.circle.author.profile_image else None
    subject = f"✨New: {title}✨"
    CircleAdvertisementEmail(
        recipient=user.email,
        link=_make_email_url(event.get_absolute_url()),
        subject=subject,
        start=start,
        event_title=event.title,
        space_title=event.circle.title,
        space_subtitle=event.circle.subtitle,
        event_details=details,
        title=title,
        subtitle=subtitle,
        author=event.circle.author.name,
        image_url=image_url,
        author_image_url=author_image_url,
        unsubscribe_url=type_url(event.circle.subscribe_url(user, subscribe=False)),
    ).send()


def send_notify_circle_signup(event: CircleEvent, user: User):
    start = _to_human_time(user, event.start)
    CircleSignupEmail(
        recipient=user.email,
        link=_make_email_url(reverse("circles:calendar", kwargs={"event_slug": event.slug})),
        start=start,
        event_title=event.circle.title,
    ).send(blocking=False)


def send_missed_event_email(event: CircleEvent, user: User):
    start = _to_human_time(user, event.start)
    title = event.title or event.circle.title
    MissedEventEmail(
        recipient=user.email,
        start=start,
        event_title=title,
        event_link=_make_email_url(event.get_absolute_url()),
    ).send(blocking=False)
