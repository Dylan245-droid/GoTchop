from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from ..models import Establishment, Review, Menu
from ..forms import ReviewForm, MenuForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.core.paginator import Paginator

# Vue pour afficher la page d'accueil
from django.shortcuts import render
from ..models import Establishment, Review

# Liste des catégories
CATEGORIES = [
    ('restaurant', 'Restaurant'),
    ('fast-food', 'Fast Food'),
    ('cafe', 'Café'),
    ('bar', 'Bar'),
    ('autre', 'Autre'),
]

def home(request):
    query = request.GET.get('q')  # Recherche
    establishments = Establishment.objects.filter(nom_r__icontains=query) if query else Establishment.objects.all()
    latest_reviews = Review.objects.select_related('etablissement', 'utilisateur').order_by('-crée_le')[:5]  # 5 derniers avis

    context = {
        'categories': CATEGORIES,  # On passe la liste des catégories
        'establishments': establishments,
        'latest_reviews': latest_reviews,
        'query': query
    }

    return render(request, 'home.html', context)


# Vue pour afficher la liste des établissements
def establishment_list(request):
    filter_type = request.GET.get("filter", "")

    establishments = Establishment.objects.annotate(
        average_rating=Avg("reviews__note"),
        review_count=Count("reviews")
    )

    # Ajout d'attributs pour le template
    for establishment in establishments:
         establishment.has_ordering = establishment.has_ordering()
         establishment.has_reservation = establishment.has_reservation()

    # Appliquer les filtres
    if filter_type == "top_rated":
        establishments = establishments.order_by("-average_rating")
    elif filter_type == "vibes":
        establishments = establishments.filter(vibes__isnull=False)
    elif filter_type == "amenities":
        establishments = establishments.filter(amenities__isnull=False)

    paginator = Paginator(establishments, 10)
    page_number = request.GET.get("page")
    establishments_page = paginator.get_page(page_number)

    return render(request, "establishments/list.html", {
        "establishments": establishments_page
    })

# Vue pour afficher le détail d'un établissement
def establishment_detail(request, establishment_id):
    establishment = get_object_or_404(Establishment, pk=establishment_id)
    reviews = establishment.reviews.all()
    menus = Menu.objects.filter(establishment=establishment)# Récupérer les menus liés à l'établissement
    

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.establishment = establishment
            new_review.utilisateur = request.user
            new_review.save()
            return redirect('establishment_detail', establishment_id=establishment.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/establishment_detail.html', {
        'establishment': establishment,
        'reviews': reviews,
        'form': form,
        "menus": menus,
    })

# Vue pour ajouter un avis à un établissement
@login_required(login_url='login')
def add_review(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)

    if request.method == "POST":
        note = request.POST.get("note")
        commentaire = request.POST.get("commentaire")
        images = request.FILES.getlist("images")  # Récupération des images

        if note and commentaire:
            review = Review.objects.create(
                utilisateur=request.user,
                etablissement=establishment,
                note=note,
                commentaire=commentaire
            )

            # Sauvegarde des images
            for image in images:
                review.images.add(image)
            review.save()

            return redirect('establishment_detail', establishment_id=establishment.id)

    return render(request, 'reviews/add_review.html', {'establishment': establishment})

# Vue pour afficher le détail d'un avis
def review_detail(request, review_id):
    return render(request, 'reviews/review_detail.html', {'review_id': review_id})

# Vue pour ajouter des données de test
def add_test_data(request):
    restaurant = Establishment.objects.create(
        nom_r="Chez Lorn",
        description="Un super resto au Gabon",
        addresse="123 Rue Libreville",
        ville="Libreville",
        categorie="restaurant"
    )
    user, created = User.objects.get_or_create(username="testuser", defaults={"password": "password123"})
    Review.objects.create(utilisateur=user, etablissement=restaurant, note=5, commentaire="Super expérience !")
    return HttpResponse("Données ajoutées avec succès !")


from django.shortcuts import render, get_object_or_404
from ..models import Establishment

def establishments_by_category(request, category):
    establishments = Establishment.objects.filter(categorie=category)
    
    context = {
        'selected_category': category,
        'establishments': establishments,
    }
    
    return render(request, 'reviews/category_list.html', context)



def category_filter(request, categorie):
    category_label = dict(Establishment.CATEGORY_CHOICES).get(categorie, "Catégorie inconnue")
    establishments = Establishment.objects.filter(categorie=categorie)

    context = {
        'selected_category': category_label,
        'establishments': establishments,
    }
    return render(request, 'reviews/category_list.html', context)

@login_required
def profile_view(request):
    return render(request, 'reviews/profile.html', {'user': request.user})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Vérifie si l'utilisateur est bien l'auteur du commentaire
    if review.utilisateur == request.user:
        review.delete()
        messages.success(request, "Votre avis a été supprimé avec succès.")
    else:
        messages.error(request, "Vous ne pouvez supprimer que vos propres avis.")

    return redirect('establishment_detail', establishment_id=review.etablissement.id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Vérifier si l'utilisateur est bien l'auteur de l'avis
    if review.utilisateur != request.user:
        messages.error(request, "Vous ne pouvez modifier que vos propres avis.")
        return redirect('establishment_detail', establishment_id=review.etablissement.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre avis a été mis à jour avec succès !")
            return redirect('establishment_detail', establishment_id=review.establishment.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


@login_required
def vote_review(request, review_id, vote_type):
    review = get_object_or_404(Review, id=review_id)
    
    if vote_type == "like":
        if request.user in review.likes.all():
            review.likes.remove(request.user)
        else:
            review.likes.add(request.user)
            review.dislikes.remove(request.user)  # Enlever le dislike si existant

    elif vote_type == "dislike":
        if request.user in review.dislikes.all():
            review.dislikes.remove(request.user)
        else:
            review.dislikes.add(request.user)
            review.likes.remove(request.user)  # Enlever le like si existant

    return JsonResponse({"likes": review.total_likes(), "dislikes": review.total_dislikes()})

@login_required
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Empêcher un utilisateur de signaler son propre avis
    if request.user == review.utilisateur:
        return JsonResponse({"error": "Vous ne pouvez pas signaler votre propre avis."}, status=400)

    if request.user in review.reports.all():
        review.reports.remove(request.user)  # Permet d'annuler un signalement
        message = "Signalement annulé."
    else:
        review.reports.add(request.user)
        message = "Avis signalé avec succès."

    return JsonResponse({"total_reports": review.total_reports(), "message": message})

def est_admin(user):
    return user.is_staff or user.is_superuser  # Seuls les admins peuvent ajouter un menu

@login_required
@user_passes_test(est_admin)
def add_menu(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)

    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.establishment = establishment
            menu.save()
            return redirect("establishment_detail", id=establishment.id)  

    else:
        form = MenuForm()

    return render(request, "reviews/add_menu.html", {"form": form, "establishment": establishment})


