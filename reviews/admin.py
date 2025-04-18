from django.contrib.gis import admin
from .models import Establishment, Review, Menu, Vibe, Amenity, EtablishmentCategory, MenuSection, Dishe


@admin.register(EtablishmentCategory)
class EtablishmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description')
        }),
    )


@admin.register(Establishment)
class EstablishmentAdmin(admin.OSMGeoAdmin):
    list_display = ("nom_r", "ville", "category", "phone_number", "website", "crée_le", "location")
    search_fields = ("nom_r", "ville", "category")
    list_filter = ("category", "ville")
    filter_horizontal = ("vibes", "amenities", "images")  # Ajout des champs ManyToMany

    fieldsets = (
        ("Informations Générales", {
            "fields": ("nom_r", "description", "addresse", "ville", "location", "category", "images")
        }),
        ("Contact", {
            "fields": ("phone_number", "website")
        }),
        ("Détails", {
            "fields": ("vibes", "amenities", "location_hours")
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


@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('establishment', 'image', 'menu_pdf')
    list_filter = ('establishment',)
    search_fields = ('nom_plat', 'establishment__nom_r')
    ordering = ('establishment',)
    filter_horizontal = ('sections',)

    fieldsets = (
        (None, {
            'fields': ('establishment', 'sections')
        }),
        ('Fichiers', {
            'fields': ('image', 'menu_pdf'),
            'description': "Ajoutez une image ou un fichier PDF pour le menu."
        }),
    )


@admin.register(Dishe)
class DisheAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'section', 'prix')
    list_filter = ('menu', 'section')
    search_fields = ('name', 'menu__nom_plat', 'section__name')
    ordering = ('menu', 'section')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'prix', 'menu', 'section')
        }),
    )
