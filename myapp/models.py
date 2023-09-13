from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='employe')
    nom = models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    adresse = models.CharField(max_length=200,default="not mentioned")
    image=models.ImageField(upload_to='profilepics/',default="profilepics/default.png",null=True,blank=True)
    is_image=models.BooleanField(default=False)
    # nuull true mean that the field is not required in the form and blank true mean that the field can be empty
    email = models.EmailField()
    role = models.CharField(max_length=100)  # Ajout de l'attribut 'role'
    etat = models.BooleanField(default=False)  # Ajout de l'attribut 'état'
    nb_accepte=models.IntegerField(default=0)
  
    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(Employe, on_delete=models.CASCADE,)
    message = models.CharField(max_length=200)
    date= models.DateTimeField(auto_now_add=True)
    is_him = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.user.username} "    
    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='client')
    nom = models.CharField(max_length=100,default="")
    prenom=models.CharField(max_length=100,default="")
    adresse = models.CharField(max_length=200,default="not mentioned")
    image=models.ImageField(upload_to='profilepics/',default="profilepics/default.png",null=True,blank=True)
    is_image=models.BooleanField(default=False)
    email = models.EmailField()
   
    etat = models.BooleanField(default=False) 
    nb_accepte=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notifications')
    message = models.CharField(max_length=200)
    link = models.URLField()  # URL to the related page
    display=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.message} notification for {self.user.username}"    

class Stagiaire(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE,null=True,blank=True)
    encadrant = models.CharField(max_length=100,default="xx")  
    faculte = models.CharField(max_length=100)  
    specialite = models.CharField(max_length=100) 


    def __str__(self):
        return self.employe.user.username
    
class Tache(models.Model):
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    etat = models.CharField(max_length=100,default="nonfait")
    description = models.TextField()
    date= models.DateTimeField(auto_now_add=True)
    travail = models.FileField(upload_to='travaux_stagiaires/',null=True)
    note=models.IntegerField(default=0)
    

    def __str__(self):
        return f"task added by {self.stagiaire.encadrant }"   


class ResponsableRH(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)

    def __str__(self):
        return self.employe.user.username

class DevLogiciel(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)
    technologies_utilisees = models.CharField(max_length=100)  

    def __str__(self):
        return self.employe.user.username
    


class Code(models.Model):
    devlogiciel = models.ForeignKey(DevLogiciel, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    fichier=models.FileField(upload_to='codes/',null=True)
    likes = models.IntegerField(default=0)
    date= models.DateTimeField(auto_now_add=True,blank=True,null=True)

    language=models.CharField(max_length=100,default="python")
    def __str__(self):
        return f"code added by {self.devlogiciel.employe.user.username}"









class GestionnaireServiceClient(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)

    def __str__(self):
        return self.employe.user.username

class Encadrant(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)
    etat = models.BooleanField(default=False) 

    def __str__(self):
        return self.employe.user.username


class Reclamation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE,null=True,blank=True)
    sujet = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reponse = models.TextField(max_length=100,default="Pas encore de réponse")

    def __str__(self):
        return f"Complaint by {self.employe.user.username}: {self.sujet}"
    


class Conge(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE,null=True,blank=True)
    raison = models.CharField(max_length=100)
    depart=models.DateField()
    fin=models.DateField()  
    reponse = models.TextField(max_length=100,default="Pas encore de réponse")
    def __str__(self):
        return f"demande de congé by {self.employe.user.username}: {self.raison}"
    


class AssuranceAutomobile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    marque = models.CharField(max_length=100)
    date_premiercirculation = models.DateField()
    usage=models.CharField(max_length=100)
    reponse = models.TextField(max_length=100,default="Pas encore pris en charge")
    def __str__(self):
        return f"Assurance Automobile {self.client.user.username}"

class AssuranceHabitation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    superficie = models.IntegerField()
    reponse = models.TextField(max_length=100,default="Pas encore pris en charge")
    def __str__(self):
        return f"Assurance Habitation {self.client.user.username}"    



# Fonctionnalités générales pour les employés :
# - Authentification et autorisation
# - faire reclamation
# - demander des congé 

# Fonctionnalités spécifiques pour chaque rôle :
# - Responsable des ressources humaines :
#   - Gestion des reclamations
#   - Gestion des congés
# - Développeur logiciel :
#   - Gestion des projets de développement( il publie don son espace des codes )
# - Stagiaire :
#   - Suivi des tâches assignées par son encendrant 
# - Encadrant :
#   - Gestion des stagiaires
#   - Suivi des projets des stagiaires(dooner une tache et la noter)
# - Gestionnaire du service client :
#   - Gestion des demandes des clients( accepter ou refuse les souscriptions )
#   - Gestion de la satisfaction client


# Fonctionnalités pour les clients :
# - Gestion des profils clients
# - Souscription en ligne



# Create your models here.
