from django.db import models
from django.contrib.auth.models import User

class Establishment(models.Model):
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('fast-food', 'Fast Food'),
        ('cafe', 'Café'),
        ('bar', 'Bar'),
        ('autre', 'Autre'),
    ]

    nom_r = models.CharField(max_length=100)
    description = models.TextField()
    addresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Correction ici ✅
    crée_le = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    image = models.ImageField(upload_to='establishments/', blank=True, null=True) 

    def __str__(self):
        return self.nom_r


class Review(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Establishment, related_name='reviews', on_delete=models.CASCADE)
    note = models.IntegerField()
    commentaire = models.TextField()
    crée_le = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews', blank=True)
    reports = models.ManyToManyField(User, related_name='reported_reviews', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
    
    def total_reports(self):
        return self.reports.count()

    def __str__(self):
        return f"Review by {self.utilisateur.username} for {self.etablissement.nom_r}"


from django.db import models

class Category(models.Model):
     CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('fast-food', 'Fast Food'),
        ('cafe', 'Café'),
        ('bar', 'Bar'),
        ('autre', 'Autre'),
    ]

     name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

     def __str__(self):
        return self.name
from django.core.exceptions import ValidationError
from django.db import models

class Menu(models.Model):
    establishment = models.ForeignKey("Establishment", on_delete=models.CASCADE, related_name="menus")
    nom_plat = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="menus/", null=True, blank=True)
    menu_pdf = models.FileField(upload_to="menus_pdfs/", null=True, blank=True)  # 📄 Ajout du PDF

    def clean(self):
        """
        Validation personnalisée : 
        - Soit une image, soit un PDF, soit les infos textuelles (nom_plat et prix) doivent être présentes.
        """
        if not self.image and not self.menu_pdf and not (self.nom_plat and self.prix):
            raise ValidationError("Vous devez fournir soit une image, soit un PDF, soit un nom de plat et un prix.")

    def __str__(self):
        return f"{self.nom_plat if self.nom_plat else 'Document Menu'} - {self.establishment.nom_r}"

    
