from django.shortcuts import render, redirect, get_object_or_404
from .models import Projet, Tache
from .forms import ProjetForm, TacheForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
import uuid


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Authentifie l'utilisateur
            return redirect('accueil')  # Redirige vers une page d'accueil
        else:
            # Identifiants incorrects
            return render(request, 'login.html', {'error': 'Identifiants invalides.'})
    return render(request, 'login.html')



@login_required
def accueil(request):
    projets = Projet.objects.filter(proprietaire=request.user)
    return render(request, 'accueil.html', {'projets': projets})

@login_required
def ajouter_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)  # NE PAS sauver directement
            projet.code = str(uuid.uuid4())[:8]  # Générer un code aléatoire court
            projet.proprietaire = request.user  # Mettre le user connecté
            projet.save()  # Maintenant on peut enregistrer
            return redirect('liste_projets')  # ou autre page
    else:
        form = ProjetForm()
    return render(request, 'ajouter_projet.html', {'form': form})


@login_required
def projet_detail(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    taches = Tache.objects.filter(projet=projet)
    return render(request, 'projet_detail.html', {'projet': projet, 'taches': taches})

@login_required
def ajouter_tache(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            tache = form.save(commit=False)
            tache.projet = projet
            tache.save()
            return redirect('projet_detail', projet_id=projet.id)
    else:
        form = TacheForm()
    return render(request, 'ajouter_tache.html', {'form': form})

@login_required
def modifier_tache(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            return redirect('projet_detail', projet_id=tache.projet.id)
    else:
        form = TacheForm(instance=tache)
    return render(request, 'modifier_tache.html', {'form': form, 'tache': tache})

@login_required
def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)
    projet_id = tache.projet.id
    tache.delete()
    return redirect('projet_detail', projet_id=projet_id)



def liste_projets(request):
    projets = Projet.objects.all()
    return render(request, 'liste_projets.html', {'projets': projets})


