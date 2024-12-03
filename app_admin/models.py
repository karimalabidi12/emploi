from django.db import models




class Role(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Departement(models.Model):
    id = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=100)
    Directeur_id = models.ForeignKey('Utilisateur', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.Nom


class Parcours(models.Model):
    id = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=100)
    Departement_id = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nom

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} {self.prenom}"




class Enseignant(models.Model):
    id = models.AutoField(primary_key=True)
    departementID = models.ForeignKey(Departement, on_delete=models.CASCADE)
    specialisation = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    date_embauche = models.DateField()

    def __str__(self):
        return f"{self.grade} - {self.specialisation}"


class Classe(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    annee_academique = models.CharField(max_length=10)
    Parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    Parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
    Nature = models.CharField(max_length=50)
    Charge = models.PositiveIntegerField()

    def __str__(self):
        return self.nom


class Absence(models.Model):
    id = models.AutoField(primary_key=True)
    etudiant_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="absences")
    Emploi_id = models.ForeignKey('EmploiCours', on_delete=models.CASCADE)
    date = models.DateField()
    justifie = models.BooleanField(default=False)
    motif = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Absence de {self.utilisateur} le {self.date}"


class InscriptionClasse(models.Model):
    id = models.AutoField(primary_key=True)
    classe_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    etudiant_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_inscription = models.DateField()

    def __str__(self):
        return f"Inscription {self.id} - Classe {self.classe_id}"


class AffectationCours(models.Model):
    id = models.AutoField(primary_key=True)
    enseignant_id = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    Matieres = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    ChargeEdu = models.PositiveIntegerField()
    AU = models.CharField(max_length=10)  # Année universitaire
    Semestre = models.PositiveIntegerField()

    def __str__(self):
        return f"Affectation {self.id}"


class LogModification(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateur_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    date_modification = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"Log {self.id} - Action {self.action}"

class EmploiCours(models.Model):
    id = models.AutoField(primary_key=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    salle = models.ForeignKey('Salle', on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    jour = models.CharField(max_length=20)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"Emploi {self.id}"



class Salle(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacite = models.PositiveIntegerField()

    def __str__(self):
        return self.nom
