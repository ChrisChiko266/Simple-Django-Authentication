from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _

import uuid


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('Email Address'), blank=True, unique=True)
    username = models.CharField(_('Username'), max_length=250, unique=True, blank=True, )
    avatar = models.ImageField(null=True, blank=True)
    first_name = models.CharField(_('First Name'), max_length=50, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now=True)
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_(
            'Designates whether a user should be treated as `is active`.'
            'Unselect this instead of manually deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('Staff'), default=False,
        help_text=_('Designates whether a user can log into the admin site.')
    )
    is_admin = models.BooleanField(default=False)

    # Specify authentication method
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    objects = UserManager()
