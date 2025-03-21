from django.contrib import admin
from .models import Establishment, Review, Menu, Vibe, Amenity

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("nom_r", "ville", "categorie", "phone_number", "website", "crée_le")
    search_fields = ("nom_r", "ville", "categorie")
    list_filter = ("categorie", "ville")
    filter_horizontal = ("vibes", "amenities")  # Ajout des champs ManyToMany

    fieldsets = (
        ("Informations Générales", {
            "fields": ("nom_r", "description", "addresse", "ville", "categorie", "image")
        }),
        ("Contact", {
            "fields": ("phone_number", "website")
        }),
        ("Détails", {
            "fields": ("vibes", "amenities", "location_hours", "popular_dishes")
        }),
    )

@admin.register(Vibe)
class VibeAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'etablissement', 'note', 'crée_le')
    search_fields = ('utilisateur__username', 'etablissement__nom_r')  # Correction des champs de recherche
    list_filter = ('note', 'crée_le')

class MenuAdmin(admin.ModelAdmin):
    list_display = ('nom_plat', 'establishment', 'prix', 'image', 'menu_pdf')  
    list_filter = ('establishment',)
    search_fields = ('nom_plat', 'establishment__nom_r')
    ordering = ('establishment', 'nom_plat')

    fieldsets = (
        (None, {
            'fields': ('establishment', 'nom_plat', 'description', 'prix')
        }),
        ('Fichiers', {
            'fields': ('image', 'menu_pdf'),
            'description': "Ajoutez une image ou un fichier PDF pour le menu."
        }),
    )

admin.site.register(Menu, MenuAdmin)