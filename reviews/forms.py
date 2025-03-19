from django import forms
from .models import Review
from .models import Menu

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
        
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nom_plat', 'description', 'prix', 'image', 'menu_pdf']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        menu_pdf = cleaned_data.get("menu_pdf")

        if image and menu_pdf:
            raise forms.ValidationError("Vous ne pouvez pas ajouter une image et un PDF en même temps.")
        
        if not image and not menu_pdf:
            raise forms.ValidationError("Vous devez ajouter soit une image, soit un PDF du menu.")
        
        return cleaned_data