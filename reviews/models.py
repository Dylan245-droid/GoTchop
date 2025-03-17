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

