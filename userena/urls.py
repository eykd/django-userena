from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from userena import views as userena_views
from userena import settings as userena_settings


VALID_USERNAME_PATTERN = getattr(settings, 'USERENA_VALID_USERNAME_PATTERN', r'[\.\w]+')


def username_url(user_url, *args, **kwargs):
    user_url = user_url.format(username_p=VALID_USERNAME_PATTERN)
    return url(user_url, *args, **kwargs)


urlpatterns = patterns('',
    # Signup, signin and signout
    url(r'^signup/$',
       userena_views.signup,
       name='userena_signup'),
    url(r'^signin/$',
       userena_views.signin,
       name='userena_signin'),
    url(r'^signout/$',
       userena_views.signout,
       name='userena_signout'),

    # Reset password
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'userena/password_reset_form.html',
        'email_template_name': 'userena/emails/password_reset_message.txt'},
       name='userena_password_reset'),
    url(r'^password/reset/done/$',
       auth_views.password_reset_done,
       {'template_name': 'userena/password_reset_done.html'},
       name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
       auth_views.password_reset_confirm,
       {'template_name': 'userena/password_reset_confirm_form.html'},
       name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$',
       auth_views.password_reset_complete,
       {'template_name': 'userena/password_reset_complete.html'}),

    # Signup
    username_url(r'^(?P<username>{username_p})/signup-complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/signup_complete.html',
        'extra_context': {'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
                          'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
       name='userena_signup_complete'),

    # Activate
    url(r'^activate/(?P<activation_key>\w+)/$',
       userena_views.activate,
       name='userena_activate'),

    # Change email and confirm it
    username_url(r'^(?P<username>{username_p})/edit/email/$',
       userena_views.email_change,
       name='userena_email_change'),
    username_url(r'^(?P<username>{username_p})/edit/email/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_change_complete.html'},
       name='userena_email_change_complete'),
    username_url(r'^(?P<username>{username_p})/edit/email/confirmed/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/email_confirm_complete.html'},
       name='userena_email_confirm_complete'),
    url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
       userena_views.email_confirm,
       name='userena_email_confirm'),

    # Disabled account
    username_url(r'^(?P<username>{username_p})/disabled/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/disabled.html'},
       name='userena_disabled'),

    # Change password
    username_url(r'^(?P<username>{username_p})/edit/password/$',
       userena_views.password_change,
       name='userena_password_change'),
    username_url(r'^(?P<username>{username_p})/edit/password/complete/$',
       userena_views.direct_to_user_template,
       {'template_name': 'userena/password_complete.html'},
       name='userena_password_change_complete'),

    # Edit profile
    username_url(r'^(?P<username>{username_p})/edit/$',
       userena_views.profile_edit,
       name='userena_profile_edit'),

    # View profiles
    username_url(r'^(?P<username>{username_p})/$',
       userena_views.profile_detail,
       name='userena_profile_detail'),
    url(r'^page/(?P<page>[0-9]+)/$',
       userena_views.ProfileListView.as_view(),
       name='userena_profile_list_paginated'),
    url(r'^$',
       userena_views.ProfileListView.as_view(),
       name='userena_profile_list'),
)
