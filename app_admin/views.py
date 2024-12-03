from .models import EmploiCours, Utilisateur,Enseignant
from .forms import * # Assure-toi que le formulaire est bien importé
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Utilisateur, Role
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def index_view(request):
    return render(request, 'index.html')
# Vue pour la page de connexion
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('index')  # Redirige vers la page d'accueil après connexion
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'login.html') 

def logout_view(request):
    logout(request)
    return redirect('login')  

def register_view(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        password = request.POST['password']
        role_nom = request.POST.get('role', 'Étudiant')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=email, password=password)
            utilisateur = Utilisateur.objects.create(
            nom=nom, prenom=prenom, email=email, mot_de_passe=password, role=Role.objects.get(nom=role_nom)
            )
            messages.success(request, "Inscription réussie ! Vous pouvez vous connecter.")
            return redirect('login')
    return render(request, 'register.html')


# Vue pour afficher l'emploi du temps d'un étudiant
def emploi_etudiant(request):
    if request.user.is_authenticated:
        # Récupérer l'utilisateur connecté
        utilisateur = Utilisateur.objects.get(email=request.user.username)
        
        # Récupérer les inscriptions de cet étudiant
        inscriptions = utilisateur.inscriptionclasse_set.all()

        # Récupérer les emplois du temps des classes de l'étudiant
        emplois = EmploiCours.objects.filter(classe__in=[inscription.classe for inscription in inscriptions])

        return render(request, 'emploi_etudiant.html', {'emplois': emplois})

    else:
        return redirect('login')  

# Vue pour afficher l'emploi du temps d'un enseignant
def emploi_enseignant(request):
    if request.user.is_authenticated:
        # Récupérer l'utilisateur connecté
        utilisateur = Utilisateur.objects.get(email=request.user.username)
        enseignant = Enseignant.objects.get(utilisateur=utilisateur)

        # Récupérer les emplois du temps de cet enseignant
        emplois = EmploiCours.objects.filter(enseignant=enseignant)

        return render(request, 'emploi_enseignant.html', {'emplois': emplois})

    else:
        return redirect('login')  # Si l'utilisateur n'est pas connecté, redirige vers la page de login



def add_salle(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde la nouvelle salle dans la base de données
            return redirect('add_salle')  # Redirige pour rafraîchir la page et afficher la liste mise à jour
    else:
        form = SalleForm()

    # Récupérer toutes les salles existantes
    salles_list = Salle.objects.all()

    return render(request, 'add_salle.html', {'form': form, 'salles_list': salles_list})


def add_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde la matière dans la base de données
            return redirect('add_matiere')  # Redirige vers la même page pour rafraîchir avec la nouvelle matière
    else:
        form = MatiereForm()

    # Récupérer toutes les matières existantes
    matieres = Matiere.objects.all()

    return render(request, 'add_matiere.html', {'form': form, 'matieres': matieres})


def add_classe(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_classe')  # Redirige vers la même page pour rafraîchir avec la nouvelle classe
    else:
        form = ClasseForm()

    # Récupère toutes les classes existantes
    classes = Classe.objects.all()

    return render(request, 'add_classe.html', {'form': form, 'classes': classes})


def add_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_departement')  # Redirige vers la même page pour rafraîchir avec le nouveau département
    else:
        form = DepartementForm()

    # Récupérer tous les départements existants
    departements = Departement.objects.all()

    return render(request, 'add_departement.html', {'form': form, 'departements': departements})


def add_parcours(request):
    if request.method == 'POST':
        form = ParcoursForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde le nouveau parcours
            return redirect('add_parcours')  # Redirige pour rafraîchir la page avec le nouveau parcours
    else:
        form = ParcoursForm()

    # Récupérer tous les parcours existants
    parcours_list = Parcours.objects.all()

    return render(request, 'add_parcours.html', {'form': form, 'parcours_list': parcours_list})


def affecter_cours(request):
    if request.method == 'POST':
        form = AffectationCoursForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde l'affectation dans la base de données
            return redirect('affecter_cours')  # Redirige pour rafraîchir la page et afficher la liste mise à jour
    else:
        form = AffectationCoursForm()

    # Récupérer toutes les affectations de cours existantes
    affectations_list = AffectationCours.objects.all()

    return render(request, 'affecter_cours.html', {'form': form, 'affectations_list': affectations_list})





def add_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_absence')
    else:
        form = AbsenceForm()

    absences_list = Absence.objects.all()

    return render(request, 'add_absence.html', {'form': form, 'absences_list': absences_list})



def liste_inscriptions(request):
    # Récupérer les étudiants et les enseignants
    etudiants = Utilisateur.objects.filter(role__nom="Étudiant")
    enseignants = Utilisateur.objects.filter(role__nom="Enseignant")
    
    context = {
        'etudiants': etudiants,
        'enseignants': enseignants
    }
    return render(request, 'liste_inscriptions.html', context)
