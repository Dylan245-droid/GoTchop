from django.urls import path
from .views.reviews import establishments_by_category
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views.reviews import (
    home, 
    establishment_list, 
    establishment_detail, 
    add_review, 
    review_detail, 
    add_test_data, 
    category_filter,
    profile_view ,
    delete_review,
    edit_review ,
    vote_review ,
    report_review ,
    add_menu ,
)

urlpatterns = [
    path('', home, name='home'),  # Page d'accueil
    path('populate/', add_test_data, name='populate_data'),  # Remplir la BD de données de test
    path('establishments/', establishment_list, name='establishment_list'),  # Liste des établissements
    path('establishment/<int:establishment_id>/', establishment_detail, name='establishment_detail'),  # Détail d'un établissement
    path('establishment/<int:establishment_id>/add_review/', add_review, name='add_review'),  # Ajouter un avis
    path('review/<int:review_id>/', review_detail, name='review_detail'),  # Détail d'un avis
    path('categorie/<str:category>/', establishments_by_category, name='categorie'),
    path('categorie/<str:category>/', category_filter, name='category_filter'),
    path('login/', auth_views.LoginView.as_view(template_name='reviews/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reviews/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reviews/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reviews/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reviews/password_reset_complete.html'), name='password_reset_complete'),
    path("profil/", profile_view, name="profile"),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('review/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('review/<int:review_id>/vote/<str:vote_type>/', vote_review, name='vote_review'),
    path('review/<int:review_id>/report/', report_review, name='report_review'),
    path("etablissement/<int:establishment_id>/ajouter_menu/", add_menu, name="add_menu"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


