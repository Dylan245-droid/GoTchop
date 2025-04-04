from datetime import datetime
from django.utils.translation import gettext as _


def cores(request):

    greetings = (
        _("Bonjour")
        if datetime.now().hour < 17
        else _("Bonsoir")
    )

    context = {
        "APP_NAME": "GoTchop",
        "GREETINGS": greetings,
        "YEAR": datetime.now().year,
    }

    return context
