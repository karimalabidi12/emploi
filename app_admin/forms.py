from django import forms
from .models import *

class EmploiCoursForm(forms.ModelForm):
    class Meta:
        model = EmploiCours
        fields = ['classe', 'enseignant', 'salle', 'matiere', 'jour', 'heure_debut', 'heure_fin']


class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'type', 'capacite']

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'Parcours', 'Nature', 'Charge']

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'annee_academique', 'Parcours']

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['Nom', 'Directeur_id']
class ParcoursForm(forms.ModelForm):
    class Meta:
        model = Parcours
        fields = ['Nom', 'Departement_id']
class AffectationCoursForm(forms.ModelForm):
    class Meta:
        model = AffectationCours
        fields = ['enseignant_id', 'Matieres', 'ChargeEdu', 'AU', 'Semestre']


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date', 'justifie', 'motif']

    utilisateur = forms.ModelChoiceField(
        queryset=Utilisateur.objects.all(),
        label="Utilisateur (Étudiant ou Enseignant)"
    )
