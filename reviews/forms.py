from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.Select(
                choices=[(i, i) for i in range(1, 6)], 
                attrs={'class': 'form-control'}
            ),  # Sélecteur de notes de 1 à 5
            'commentaire': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),  # Zone de texte avec 4 lignes par défaut
        }
