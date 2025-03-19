from django.contrib import admin
from .models import Establishment, Review, Menu

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ('nom_r', 'categorie', 'ville', 'crée_le')  # Colonnes affichées dans l'admin
    search_fields = ('nom_r',  'ville')  # Recherche possible sur ces champs
    list_filter = ('categorie', 'ville')  # Filtres sur la droite de l'admin

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