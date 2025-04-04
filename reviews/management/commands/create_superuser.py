from django.contrib.auth import get_user_model
import os
import django
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser if it doesn't exist."

    def handle(self, *args, **kwargs):
        username = os.getenv("DEFAULT_SUPERUSER_USERNAME")
        email = os.getenv("DEFAULT_SUPERUSER_EMAIL")
        password = os.getenv("DEFAULT_SUPERUSER_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                _("Superutilisateur “%(username)s” créé avec succès. !") % {'username': username}))
        else:
            self.stdout.write(self.style.WARNING(
                _("Le superutilisateur “%(username)s” existe déjà. !") % {'username': username}))
