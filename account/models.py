from django.db import models
from .managers import AccountManager
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from utils import generate_serie

# Create your models here.


class Account(AbstractUser):

    objects = AccountManager()

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("Un utilisateur avec cet email existe déjà."),
        },
    )

    is_active = models.BooleanField(default=True)

    @property
    def get_groups(self):
        data = []
        for group in self.groups.all():
            if group.name not in data:
                data.append(group.name)
        return data

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name.upper()} {self.first_name.title()}"
        else:
            return self.username

    def __str__(self):
        return self.get_full_name


class OTPCode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """ Vérifie si le code est valide (ex : expiration en 5 minutes) """
        return datetime.datetime.now(datetime.timezone.utc) - self.created_at < datetime.timedelta(minutes=5)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == "" :
            self.code = generate_serie(6)
        super(OTPCode, self).save(*args, **kwargs)
