from reviews.models import EtablishmentCategory, Amenity, Vibe
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = "Populates the default etablishment category data"

    def handle(self, *args, **options):

        categories = [
            {
                "name": "Restaurant",
                "description": "Un établissement raffiné qui offre une cuisine élaborée dans un cadre chaleureux, idéal pour des repas conviviaux et gourmands."
            },
            {
                "name": "Fast Food",
                "description": "Un lieu dynamique et accessible où l'on sert rapidement des plats savoureux et pratiques, parfait pour une pause déjeuner express."
            },
            {
                "name": "Café",
                "description": "Un espace cosy et décontracté pour savourer cafés, thés et douceurs, propice à la détente et aux échanges."
            },
            {
                "name": "Bar",
                "description": "Un établissement animé offrant une sélection de cocktails, bières et apéritifs, idéal pour des soirées festives et conviviales."
            }
        ]

        amineties = [
            "Wi-Fi Gratuit", "Terrasse ou Espace Extérieur", "Parking Disponible", "Animations et Musique Live", "Coin Enfants et Menus Adaptés"
        ]

        vibles = [
            "Décontractée et Chill", "Élégante et Sophistiquée", "Festive et Dynamique", "Cosy et Intime", "Familiale et Conviviale"
        ]

        for category in categories:
            if EtablishmentCategory.objects.filter(name=category["name"]).exists() is False:
                EtablishmentCategory.objects.create(
                    name=category["name"],
                    description=category["description"]
                )

                self.stdout.write(self.style.SUCCESS(
                    _("Categorie “%(value)s” ajoutée à la base de données !") % {'value': category["name"]}))
        
        for amenity in amineties:
            if Amenity.objects.filter(name=amenity).exists() is False:
                Amenity.objects.create(name=amenity)

                self.stdout.write(self.style.SUCCESS(
                    _("Service “%(value)s” ajoutée à la base de données !") % {'value': amenity}))

        for vibe in vibles:
            if Vibe.objects.filter(name=vibe).exists() is False:
                Vibe.objects.create(name=vibe)

                self.stdout.write(self.style.SUCCESS(
                    _("Ambiance “%(value)s” ajoutée à la base de données !") % {'value': vibe}))