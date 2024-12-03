from django.urls import path
from . import views  

urlpatterns = [
   path('', views.index_view, name='index'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('emploi_etudiant/', views.emploi_etudiant, name='emploi_etudiant'),
    path('emploi_enseignant/', views.emploi_enseignant, name='emploi_enseignant'),
    path('add_salle/', views.add_salle, name='add_salle'),
    path('add_matiere/', views.add_matiere, name='add_matiere'),
    path('add_classe/', views.add_classe, name='add_classe'),
    path('add_departement/', views.add_departement, name='add_departement'),
    path('add_parcours/', views.add_parcours, name='add_parcours'),
    path('affecter_cours/', views.affecter_cours, name='affecter_cours'),
    path('add_absence/', views.add_absence, name='add_absence'),
    path('liste_inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),

]