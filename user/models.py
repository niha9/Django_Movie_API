from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _



class User(AbstractUser):
    username             = models.CharField(max_length=25, unique=True)
    password             = models.CharField(max_length=25)
    first_name           = None
    last_name            = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


