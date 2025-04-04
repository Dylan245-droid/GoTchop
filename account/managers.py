from django.db.models import QuerySet
from django.contrib.auth.models import UserManager


class AccountManager(UserManager):

    def valids_account(self) -> QuerySet:
        queryset = self.get_queryset()
        return queryset.filter(is_active=True)
