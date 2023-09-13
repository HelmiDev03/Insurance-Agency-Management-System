import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django
django.setup()

import sys
import re 

def validate_techused(techused):
    # Define the regex pattern for the desired format
    pattern = r"^(SpringBoot|Django|NodeJs|Flask)(\|(SpringBoot|Django|NodeJs|Flask))*$"

    # Check if the techused variable matches the pattern
    if re.match(pattern, techused):
        # Split the techused string by "|" to get individual languages
        languages = techused.split("|")

        # Check if at least one of the valid languages is present
        valid_languages = {"SpringBoot", "Django", "NodeJs", "Flask"}
        if any(lang in valid_languages for lang in languages):
            return True

    return False


from django.contrib.auth.models import User
from myapp.models import Employe,Client,Stagiaire,DevLogiciel,ResponsableRH,GestionnaireServiceClient,Encadrant


'''
1)if want to add a ResponsableRH then you must follow this format
Employe,username,password,nom,prenom,adresse,email,ResponsableRH,"","",""


2)if you want to add a GestionnaireServiceClient you must follow this format
Employe,username,password,nom,prenom,adresse,email,GestionnaireServiceClient,"","",""


3)if you want to add a Encadrant you must follow this format
Employe,username,password,nom,prenom,adresse,email,Encadrant,"","",""


4)if you want to add a stagiaire you must follow this format
Employe,username,password,nom,prenom,adresse,email,Stagiaire,specialite,faculte,encadrant_username

5)if you want to add a DevLogiciel you must follow this format
make sure techused must be with format like x|y|z|t (we need at least one ) and w,y,z,t must be in ( SpringBoot, Django,NodeJS, Flask)
for exemple  techuyed = SpringBoot|Django|NodeJS|Flask or techused = SpringBoot|Django|NodeJS or techsyed = SpringBoot|Django , etc..
Employe,username,password,nom,prenom,adresse,email,DevLogiciel,technologies_utilisees,"",""

6) if you want to add a Client you must follow this format
Client,username,password,nom,prenom,adresse,email,"","","",""












'''












def create_objects_from_text_file(input):
    path = f'C:\\Users\\helmi\\OneDrive\\Desktop\\pfa2023\\myenv\\myproject\\{input}.txt'


    print(path)
    file=open(path,'r')

    lines = file.readlines()


    for line in lines:
        if line.strip().split(',') !=['']:
            print(f'------------------Query Number {lines.index(line)}------------------')
    
            model_name, username, password, first_name, last_name, address, email, role,specialite_or_tech_used,faculte,encadrent = line.strip().split(',')
            print(f"Trying to create {model_name} with username = {username}")
            if User.objects.filter(username=username).exists():
                print(f"user {username}  already exists , error in line {lines.index(line)} in your text file")
                continue
        

            user = User.objects.create_user(username=username, password=password)

            user.save()
            user_created = User.objects.get(username=username)
            if Employe.objects.filter(email=email).exists() or Client.objects.filter(email=email).exists():
                print(f"{email} already exists , error in line {lines.index(line)} in your text file")
                user_created.delete()
                continue
        

            if model_name == 'Employe':
                if role not in ['ResponsableRH', 'Stagiaire', 'GestionnaireServiceClient', 'Encadrant', 'DevLogiciel']:
                    print("role must be in ['ResponsableRH', 'Stagiaire', 'GestionnaireServiceClient', 'Encadrant', 'DevLogiciel'] , error in line {lines.index(line)} in your text file")
                    user_created.delete()
                    continue
            
                
                employe = Employe.objects.create(user=user_created, nom=last_name, prenom=first_name, adresse=address, email=email, role=role)
                employe.etat = True
                employe.save()
                if role == 'Stagiaire':
                    if Encadrant.objects.filter(employe__user__username=encadrent).exists():
                        Stagiaire.objects.create(employe=employe, faculte=faculte, specialite=specialite_or_tech_used, encadrant=encadrent)
                    
                    else:
                        print(f"There is no encadrent with username = {encadrent}, error in line {lines.index(line)} in your text file")
                        user_created.delete()
                        continue
                
                
                elif role=='DevLogiciel':
                    if validate_techused(specialite_or_tech_used):
                        devlogiciel=DevLogiciel.objects.create(employe=employe,technologies_utilisees =specialite_or_tech_used)
                        devlogiciel.save()    
                
                    else:
                        print(f"techused must be with format like x|y|z|t (we need at least one ) and w,y,z,t must be in ( SpringBoot, Django,NodeJS, Flask) , error in line {lines.index(line)} in your text file")
                        user_created.delete()
                        continue 
            
                elif role=='ResponsableRH':
                    Responsablerh=ResponsableRH.objects.create(employe=employe)    
                    Responsablerh.save()
                

                elif role=='GestionnaireServiceClient':
                    GestionnaireServiceClient=GestionnaireServiceClient.objects.create(employe=employe)    
                    GestionnaireServiceClient.save()
                

                elif role=='Encadrant':
                    Encadrant=Encadrant.objects.create(employe=employe)    
                    Encadrant.save()        
                print(f"{model_name } {(role)} {username} added successfully")  
                print('----------------------------------')
            

            elif model_name == 'Client':
                client = Client.objects.create(user=user_created, nom=last_name, prenom=first_name, adresse=address, email=email)
                client.etat = True
                client.save()
                print(f"{model_name } {username} added successfully")  
            
            else:
                print("model_name must be in ['Employe', 'Client'] , error in line {lines.index(line)} in your text file")
                user_created.delete()
                
                continue

    file.close()

    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py filename.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    create_objects_from_text_file(input_file)       

        
