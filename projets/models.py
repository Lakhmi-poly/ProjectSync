from django.db import models
from django.contrib.auth.models import User

class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=10, unique=True)
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Tache(models.Model):
    STATUTS = [
        ('AF', 'À faire'),
        ('EC', 'En cours'),
        ('TE', 'Terminée'),
    ]
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_limite = models.DateField()
    statut = models.CharField(max_length=2, choices=STATUTS, default='AF')
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre
