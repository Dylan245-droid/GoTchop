from django.db import models
from django.core.exceptions import ValidationError
from account.models import Account
from django.contrib.gis.db import models


class Image(models.Model):
    path = models.ImageField(
        upload_to='images/', blank=True, null=True
    )

    def __str__(self):
        return self.path


class EtablishmentCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categorie d\'établissement'
        verbose_name_plural = 'Categories d\'établissement'


class Establishment(models.Model):

    nom_r = models.CharField("Nom",max_length=100)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    addresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    crée_le = models.DateTimeField(auto_now_add=True)
    location = models.PointField(verbose_name="Coordonnées GPS", blank=True, null=True)  # Stocke les coordonnées GPS (longitude, latitude)

    # Contact
    phone_number = models.CharField("N° de téléphone", max_length=20, blank=True, null=True)
    website = models.URLField("Site web", blank=True, null=True)

    location_hours = models.TextField("Horaires", blank=True, null=True)  # ⏰ Horaires d'ouverture
    # popular_dishes = models.TextField("Plats populaires", blank=True, null=True)  # 🍽 Plats populaires

    # foreign key
    category = models.ForeignKey(
        EtablishmentCategory, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='establishments')
    vibes = models.ManyToManyField(
        'Vibe', blank=True, related_name='establishments')  # 🎭 What's the vibe
    amenities = models.ManyToManyField(
        'Amenity', blank=True, related_name='establishments')  # ✅ Commodités
    images = models.ManyToManyField(Image, blank=True)

    def has_amenity(self, amenity_name):
        """ Vérifie si l'établissement possède une amenity spécifique """
        return self.amenities.filter(name=amenity_name).exists()

    def has_ordering(self):
        """ Vérifie si l'établissement permet les commandes """
        return self.has_amenity("Pas besoin de réserver🚶‍♂️")

    def has_reservation(self):
        """ Vérifie si l'établissement propose des réservations """
        return self.has_amenity("Réservations acceptées 📅")

    def __str__(self):
        return self.nom_r

    class Meta:
        verbose_name = 'Etablissement'
        verbose_name_plural = 'Etablissements'


class Vibe(models.Model):
    # Ex: Moderate Noise, Casual, Good for Groups...
    name = models.CharField(max_length=100, verbose_name="Nom")
    icon = models.ImageField(upload_to='vibes_icons/',
                             blank=True, null=True)  # Icône/image associée

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ambiance'
        verbose_name_plural = 'Ambiances'


class Amenity(models.Model):
    # Ex: Offers Delivery, Vegan Options...
    name = models.CharField(max_length=100, verbose_name="Nom")
    icon = models.ImageField(upload_to='amenities_icons/',
                             blank=True, null=True)  # Icône/image associée

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Review(models.Model):
    utilisateur = models.ForeignKey(Account, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(
        Establishment, related_name='reviews', on_delete=models.CASCADE)
    note = models.IntegerField()
    commentaire = models.TextField()
    crée_le = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        Account, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(
        Account, related_name='disliked_reviews', blank=True)
    reports = models.ManyToManyField(
        Account, related_name='reported_reviews', blank=True)
    images = models.ManyToManyField(
        Image, related_name='reviews', blank=True
    )

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_reports(self):
        return self.reports.count()

    def __str__(self):
        return f"Review by {self.utilisateur.username} for {self.etablissement.nom_r}"

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

class MenuSection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Section de menu'
        verbose_name_plural = 'Sections de menus'


class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du menu")
    image = models.ImageField(upload_to="menus/", null=True, blank=True)
    menu_pdf = models.FileField(
        upload_to="menus_pdfs/", null=True, blank=True)  # 📄 Ajout du PDF

    # foreign keys
    establishment = models.ForeignKey(
        "Establishment", on_delete=models.CASCADE, related_name="menus", null=True)
    sections = models.ManyToManyField(
        MenuSection, related_name='menus', blank=True
    )

    def clean(self):
        """
        Validation personnalisée :
        - Soit une image, soit un PDF, soit les infos textuelles (nom_plat et prix) doivent être présentes.
        """
        if not self.image and not self.menu_pdf and not (self.nom_plat and self.prix):
            raise ValidationError(
                "Vous devez fournir soit une image, soit un PDF, soit un nom de plat et un prix.")

    def __str__(self):
        return f"{self.nom_plat if self.nom_plat else 'Document Menu'} - {self.establishment.nom_r}"


class Dishe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField(Image, related_name='images_dishes', blank=True)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_dishes', null=True)
    section = models.ForeignKey(
        MenuSection, on_delete=models.CASCADE, related_name='section_dishes', null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'
