from django.db import models

# parent -- enfant-- staff
class Parent(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    adresse = models.TextField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Staff(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    #groupe_responsable = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
class Enfant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Feminin')])
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    educateur = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    groupe = models.CharField(max_length=50)
    date_inscription = models.DateField(auto_now_add=True)

    allergies = models.TextField(blank=True)
    remarques_medicales = models.TextField(blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"