from django.utils.translation import gettext_lazy as _

from account.managers import PeopleManager
from account.models.user import User


class ProxyUser(User):
    """Proxy model for User with custom manager"""

    people: PeopleManager = PeopleManager()

    class Meta:
        proxy = True
        ordering = ("-pk",)
        verbose_name = _("Proxy User")
        verbose_name_plural = _("Proxy Users")
