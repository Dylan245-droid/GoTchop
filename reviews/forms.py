from django import forms
from .models import Review
from .models import Menu

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['note', 'commentaire']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note'].label = 'Note (1-5)'
        self.fields['commentaire'].label = 'Commentaire'

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'image', 'menu_pdf']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        menu_pdf = cleaned_data.get("menu_pdf")

        if image and menu_pdf:
            raise forms.ValidationError("Vous ne pouvez pas ajouter une image et un PDF en même temps.")

        if not image and not menu_pdf:
            raise forms.ValidationError("Vous devez ajouter soit une image, soit un PDF du menu.")

        return cleaned_data
