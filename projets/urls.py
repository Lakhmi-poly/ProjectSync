from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('projet/ajouter/', views.ajouter_projet, name='ajouter_projet'),
    path('projet/<int:projet_id>/', views.projet_detail, name='projet_detail'),
    path('projet/<int:projet_id>/tache/ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('tache/<int:tache_id>/modifier/', views.modifier_tache, name='modifier_tache'),
    path('tache/<int:tache_id>/supprimer/', views.supprimer_tache, name='supprimer_tache'),
]