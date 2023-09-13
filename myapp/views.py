from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User, auth
from .models import Employe,Stagiaire,ResponsableRH,DevLogiciel,GestionnaireServiceClient,Encadrant,Client,Reclamation,Conge,Code,Tache,AssuranceAutomobile,AssuranceHabitation,Notification,Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# pygments is a module for code highlight
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from django.db.models import Count,Q
import json
#Jsonresponse
from django.http import JsonResponse
from django.db.models.functions import Coalesce
from  .filecheck import checkfile


    

@login_required(login_url='login')
def notifications(request):
    user=request.user
    if Employe.objects.filter(user=user).exists():
        employe = Employe.objects.get(user=user)
        notifdata= Notification.objects.filter(user=user).order_by('-created_at')
        role=""
        stg=None
        if employe.role == "Encadrant":
            
           
            role="icadri"

 
      
 
        return render(request,'dashboard/notifications.html',{'notifdata':notifdata,'employe':employe,'role':role,})
    elif Client.objects.filter(user=user).exists():
        client = Client.objects.get(user=user)
        notifdata= Notification.objects.filter(user=user).order_by('-created_at')
      
        
        return render(request,'dashboard/notifications.html',{'notifdata':notifdata,'client':client})

@login_required(login_url='login')
def supprimer_notification(request,pk):
    Notification.objects.filter(id=pk).delete()
    return redirect('notifications')
    








def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

'''
    color: #b20a1c;
    background-color: #d7b0b0;
'''

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.success(request,'Username ou mot de passe incorrect')
                return redirect('login')
        else:

            return render(request,'login/login.html')
        
def faceid(request):
    return render(request,'login/faceid.html')



def employeeclient(request):
   
    return render(request,'signup/emloyeeclient.html')




def signupemploye(request):
    encarents=Encadrant.objects.all()
    if request.method=='POST':
      
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email'] 
        adress=request.POST['adresse']
        position=request.POST.get('position')
    
        password1=request.POST['password1']
        password2=request.POST['password2']
        print(request.POST)
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.success(request,'Username déja pris')
                return redirect('signupemploye')
            elif Employe.objects.filter(email=email).exists() or Client.objects.filter(email=email).exists():
                messages.success(request,'Email déja pris')
                return redirect('signupemploye')
            elif len(password1)<5:
                messages.success(request,'le mot de passe doit etre 5 charachters au moins')
                return redirect('signupemploye')
            elif len(password1)>16:
                messages.success(request,'le mot de passe doit etre 16 charachters au plus')
                return redirect('signupemploye')
            elif len(username)<4:
                messages.success(request,'username dit etre 4 charachters au moins')
                return redirect('signupemploye')
            elif len(username)>16:
                messages.success(request,'username doit etre 16 charachters au plus')
                return redirect('signupemploye')
            elif len(first_name)<4:
                messages.success(request,'first name doit etre 4 charachters au moins')
                return redirect('signupemploye')
            elif len(first_name)>16:
                messages.success(request,'first name doit etre 16 charachters au plus')
                return redirect('signupemploye')
            elif len(last_name)<4:
                messages.success(request,'last name doit etre 4 charachters au moins')
                return redirect('signupemploye')
            elif position not in ['Stagiaire','DevLogiciel','ResponsableRH','GestionnaireServiceClient','Encadrant']:
                messages.success(request,'tu doit choisir votre position')
                return redirect('signupemploye')
        
            
            else:
                user=User.objects.create_user(username=username,password=password1)
                user.save()
                user_model = User.objects.get(username=username)
                if 'image' in request.FILES:
                    image= request.FILES['image']
                    if not checkfile(image):   
                        print('not valid image')              
                        messages.success(request,'veuillez choisir une image valide')
                        user_model.delete()
                        return redirect('signupemploye') 

                    employee=Employe.objects.create(user=user_model,nom=last_name,prenom=first_name,adresse=adress,email=email,role=position,image=image,is_image=True)
                else:
                    employee=Employe.objects.create(user=user_model,nom=last_name,prenom=first_name,adresse=adress,email=email,role=position,is_image=False)
                
                employee.save()
                #loginthe user
                auth.login(request,user_model)
                if position=='Stagiaire':
                    return redirect('signupstagiaire',employee.id)
                elif position =='DevLogiciel':
                    return  redirect('signupdevlogiciel',employee.id)
                elif position =='ResponsableRH':
                    
                    rh_user=ResponsableRH.objects.create(employe=employee)
                    rh_user.save()
                    #auth login rh
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('home')
                elif position =='GestionnaireServiceClient':
                    client_user=GestionnaireServiceClient.objects.create(employe=employee)
                    client_user.save()
                    #auth login client
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('home')
                elif position =='Encadrant':
                    encadrant_user=Encadrant.objects.create(employe=employee)
                    encadrant_user.save()
                    #auth login client
                    user = auth.authenticate(username=username,password=password1)
                    auth.login(request,user)
                    return redirect('home')
        else:
            messages.success(request,'password not matching')
            return redirect('signupemploye')       
                    


               
      
    else:

        return render(request,'signup/signupemployee.html',{'encarents':encarents})
    

def signupstagiaire(request,employeeid):
    encadrant=Encadrant.objects.all()
    #if no encadrant in db , encadrent will be null

    if request.method=='POST':
        specialite = request.POST['specialite']
        faculte = request.POST['faculte']
        if specialite=='' or len(specialite)<2:
            messages.success(request,'specialite est obligatoire')
            return redirect('signupstagiaire',employeeid)
        if faculte=='' or len(faculte)<2:
            messages.success(request,'faculte est obligatoire')
            return redirect('signupstagiaire',employeeid)
        encadrant_choisi=request.POST.get('encadrant')
      
        employe=Employe.objects.get(id=employeeid)
        
        employe_stagiaire=Stagiaire.objects.create(employe=employe,specialite=specialite,faculte=faculte,encadrant=encadrant_choisi)   
        employe_stagiaire.save()
        #auth login stagiare
        user = auth.authenticate(username=employe.user.username,password=employe.user.password)
        auth.login(request,user)
        return redirect('home') 
    else:    
        if encadrant:
            return render(request,'signup/singup_stagaire.html',{'encadrants':encadrant,'employeeid':employeeid})
        else:
            return render(request,'signup/singup_stagaire.html',{'employeeid':employeeid})
       
    


def signupdevlogiciel(request,employeeid):
  
    if request.method=='POST':
        languages=request.POST.getlist('technology')
        employe_dev=Employe.objects.get(id=employeeid)
        #tranfrom list to string
        languages = '|'.join(languages)
        
        dev=DevLogiciel.objects.create(employe=employe_dev,technologies_utilisees=languages)
        dev.save()
        #auth login stagiare
        user = auth.authenticate(username=employe_dev.user.username,password=employe_dev.user.password)
        auth.login(request,user)
        return redirect('home')
    else:
        return render(request,'signup/signup_devlogiciel.html',{'employeeid':employeeid})



def signupclient(request):
    client=None
    if request.method=='POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email'] 
        adress=request.POST['adresse']
        password=request.POST['password']
        password1=request.POST['password1']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.success(request,'Username déja pris')
                return redirect('signupclient')
            elif Client.objects.filter(email=email).exists() or Employe.objects.filter(email=email).exists():
                messages.success(request,'Email déja pris')
                return redirect('signupclient')
            elif len(password1)<5:
                messages.success(request,'le mot de passe doit etre 5 charachters au moins')
                return redirect('signupclient')
            elif len(password1)>16:
                messages.success(request,'le mot de passe doit etre 16 charachters au plus')
                return redirect('signupclient')
            elif len(username)<4:
                messages.success(request,'username dit etre 4 charachters au moins')
                return redirect('signupclient')
            elif len(username)>16:
                messages.success(request,'username doit etre 16 charachters au plus')
                return redirect('signupclient')
            elif len(first_name)<4:
                messages.success(request,'first name doit etre 4 charachters au moins')
                return redirect('signupclient')
            elif len(first_name)>16:
                messages.success(request,'first name doit etre 16 charachters au plus')
                return redirect('signupclient')
            elif len(last_name)<4:
                messages.success(request,'last name doit etre 4 charachters au moins')
                return redirect('signupclient')
         
        
            
            else:
                user=User.objects.create_user(username=username,password=password1)
                user.save()
                user_model = User.objects.get(username=username)
                if 'image' in request.FILES:
                    image= request.FILES['image']
                    if not checkfile(image):   
                        print('not valid image')              
                        messages.success(request,'veuillez choisir une image valide')
                        user_model.delete()
                        return redirect('signupclient') 
                    client=Client.objects.create(user=user_model,nom=last_name,prenom=first_name,adresse=adress,email=email,image=image,is_image=True)
                else:
                    client=Client.objects.create(user=user_model,nom=last_name,prenom=first_name,adresse=adress,email=email,is_image=False)
                client.save()
                auth.login(request,user_model)
                return redirect('home')
    else:
        return render(request,'signup/signupclient.html')     
    




@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')










@login_required(login_url='login')
def home(request):
    notifdata={}
    user = request.user
    nb_employes=len(Employe.objects.all())
    nb_clients=len(Client.objects.all())
    dataofreclamation = Employe.objects.values('role').annotate(count=Count('reclamation')).order_by('-count')
    dataofconge = Employe.objects.values('role').annotate(count=Count('conge', filter=Q(conge__reponse="oui"))).order_by('-count')
    # Pour classer les souscriptions par usage (privée d'abord, puis utilitaire)
    usages = ['privée', 'utilitaire']  # List of all possible usages
    souscriptions_oui_par_usage = AssuranceAutomobile.objects.filter(reponse='ok').values('usage').annotate(count=Coalesce(Count('id'), 0)).order_by('usage')
    souscriptions_oui_par_type = AssuranceHabitation.objects.filter(reponse='ok').values('type').annotate(count=Coalesce(Count('id'), 0)).order_by('type')

    date_employe=Employe.objects.values('role').annotate(count=Count('id'))

    technologies = ['SpringBoot', 'Django', 'NodeJs', 'Flask']
    data_dev=[{'technologies_utilisees': 'SpringBoot', 'count': 0}, {'technologies_utilisees': 'Django', 'count': 0}, {'technologies_utilisees': 'NodeJs', 'count': 0}, {'technologies_utilisees': 'Flask', 'count': 0}]
    for technology in technologies:
        count = DevLogiciel.objects.filter(technologies_utilisees__icontains=technology).count()
        for dict in data_dev:
            if dict['technologies_utilisees'] == technology:
                dict['count'] = count
                
    

    
    '''
    SELECT employe.role,  COUNT(*) FROM conge
    WHERE conge.employe_id = employe.id AND conge.reponse = 'oui')
    FROM employe ;

    '''
    #dataofreclamation is a list of dict like this 
    ''' [  {'role': 'Encadrant', 'count': 8},
           {'role': 'GestionnaireServiceClient', 'count': 1},
           {'role': 'DevLogiciel', 'count': 1},
           {'role': 'Stagiaire', 'count': 0},
           {'role': 'ResponsableRH', 'count': 0}] 
    
    SELECT employe.role, COUNT(reclamation.id) AS count
    FROM employe, reclamation
    WHERE employe.id = reclamation.employe.id
    GROUP BY employe.role;
    ORDER BY COUNT(reclamation.id) DESC;

    '''

    # Prepare the data for the chart
    labels_reclam = [item['role'] for item in dataofreclamation]
    counts_reclam = [item['count'] for item in dataofreclamation]
     # Convert the data to JSON format to be passed to the template
    chart_data_reclam = json.dumps({'labels': labels_reclam, 'data': counts_reclam})
    
    labels_conge=[item['role'] for item in dataofconge]
    counts_conge=[item['count'] for item in dataofconge]
    chart_data_conge=json.dumps({'labels': labels_conge, 'data': counts_conge})
    
    labels_sousc=[item['usage'] for item in souscriptions_oui_par_usage]
    counts_sousc=[item['count'] for item in souscriptions_oui_par_usage]
    chart_data_sousc=json.dumps({'labels': labels_sousc, 'data': counts_sousc})


    labels_sous_hab=[item['type'] for item in souscriptions_oui_par_type]
    counts_sous_hab=[item['count'] for item in souscriptions_oui_par_type]
    chart_data_sous_hab=json.dumps({'labels': labels_sous_hab, 'data': counts_sous_hab})
   

    labels_emp=[item['role'] for item in date_employe]
    counts_emp=[item['count'] for item in date_employe]
    chart_data_emp=json.dumps({'labels': labels_emp, 'data': counts_emp})


    labels_dev = [item['technologies_utilisees'] for item in data_dev]
    counts_dev = [item['count'] for item in data_dev]
    chart_data_dev = json.dumps({'labels': labels_dev, 'data': counts_dev})



    automobile_clients_count = AssuranceAutomobile.objects.filter(reponse='ok').values('client__id').count()
    
    # Get the count of distinct clients for each type of AssuranceHabitation
    habitation_clients_count = AssuranceHabitation.objects.filter(reponse='ok').values('client__id').count()

    data_assurances = [
        {'type': 'Automobile', 'count': automobile_clients_count},
        {'type': 'Habitation', 'count': habitation_clients_count}
    ]
    labeslsassur=[item['type'] for item in data_assurances]
    countsassur=[item['count'] for item in data_assurances]
    chart_data_assurance=json.dumps({'labels': labeslsassur, 'data': countsassur})


    if Employe.objects.filter(user=user).exists():
        employe = Employe.objects.get(user=user)
        
        return render(request, 'dashboard/index.html', {'user': user,
                                                    'nb_employes':nb_employes,
                                                    'nb_clients':nb_clients,
                                                    'chart_data_reclamation': chart_data_reclam,
                                                    'chart_data_conge':chart_data_conge,
                                                    'chart_data_sousc':chart_data_sousc,
                                                    'chart_data_sous_hab':chart_data_sous_hab,
                                                    'chart_data_emp':chart_data_emp,
                                                    'chart_data_dev':chart_data_dev,
                                                    'chart_data_assurance':chart_data_assurance,
                                                    'user_type': 'Employe',
                                                    'employe': employe ,
                                                    
                                                

                                                    
                                                        } 
                )
    elif Client.objects.filter(user=user).exists():
        client = Client.objects.get(user=user)
        return render(request, 'dashboard/index.html', {'user': user,
                                                    'nb_employes':nb_employes,
                                                    'nb_clients':nb_clients,
                                                    'chart_data_reclamation': chart_data_reclam,
                                                    'chart_data_conge':chart_data_conge,
                                                    'chart_data_sousc':chart_data_sousc,
                                                    'chart_data_sous_hab':chart_data_sous_hab
                                                    ,'chart_data_emp':chart_data_emp,
                                                    'chart_data_dev':chart_data_dev,
                                                    'chart_data_assurance':chart_data_assurance
                                                    ,'user_type': 'Client',
                                                    'client': client
                                                        }
                )

    







@login_required(login_url='login')
def profile(request):
    user = request.user
    
    # Check if the user is an Employe
    if Employe.objects.filter(user=user).exists():
        employe = Employe.objects.get(user=user)
        if employe.role == 'Stagiaire':
            stagiare=Stagiaire.objects.get(employe=employe)
            print("Stagiaire faculte:", stagiare.faculte)
            print("Stagiaire specialite:", stagiare.specialite)
            return render(request, 'dashboard/settings.html', {'user_type': 'Employe', 'employe': employe,'role':'stagiare','stagiare':stagiare})
        elif employe.role=="DevLogiciel":
            devlogiciel = DevLogiciel.objects.get(employe=employe)
            listoflanguages=devlogiciel.technologies_utilisees.split("|")
            print(listoflanguages)
            return render(request, 'dashboard/settings.html', {'user_type': 'Employe', 'employe': employe,'role':'devlogiciel','devlogiciel':devlogiciel,'listoflanguages': listoflanguages})
        else:

            return render(request, 'dashboard/settings.html', {'user_type': 'Employe', 'employe': employe , 'role':""})
    
    # Check if the user is a Client
    elif Client.objects.filter(user=user).exists():
        client = Client.objects.get(user=user)
        return render(request, 'dashboard/settings.html', {'user_type': 'Client', 'client': client})
    
    # Check if the user is a Stagiaire
   
    
    # If the user type is not found, return an error message
    else:
        return render(request, 'dashboard/settings.html', {'error': 'User type not found'})


   

@login_required(login_url='login')  
def profileupdate(request):
    user = request.user  # Assuming the user is authenticated
    client=None
    if Employe.objects.filter(user=user).exists():
        employee = Employe.objects.get(user=user)
        if request.method=='POST':
            
            employee.nom = request.POST['nom']
            employee.prenom = request.POST['prenom']
            employee.adresse = request.POST['adresse']
            
       
            if  user.username != request.POST['username']:
                if ( User.objects.filter(username=request.POST['username'].lower()).exists() or User.objects.filter(email=request.POST['email'].upper()).exists()) or User.objects.filter(username=request.POST['username']).exists():
                    messages.success(request,'Username déja utilisé')   
                    return redirect('profile')


            if employee.email != request.POST['email'].upper() and employee.email != request.POST['email'].lower():    
                if (Client.objects.filter(email=request.POST['email'].lower()).exists() or Client.objects.filter(email=request.POST['email'].upper()).exists() or Employe.objects.filter(email=request.POST['email'].lower()).exists() or Employe.objects.filter(email=request.POST['email'].upper()).exists()) and client.email != request.POST['email'].lower() :
                    messages.success(request,'Email deja utilisé')   
                    return redirect('profile')
            employee.email = request.POST['email']
            user.username = request.POST['username']   
            if 'image' in request.FILES:
                if checkfile(request.FILES['image']):
                    employee.image = request.FILES['image']
                    employee.is_image = True
                else:
                    messages.success(request,'veuillez choisir une image valide')
                    return redirect('profile')    
            user.save()
            employee.save()
            if employee.role == 'Stagiaire':
                stagiaire = Stagiaire.objects.get(employe=employee)
                stagiaire.faculte = request.POST['faculte']
                stagiaire.specialite = request.POST['specialite']
                stagiaire.save()
         
            messages.success(request,'le profile a été modifié avec succés') 
            return redirect('profile') 
        else:
            return redirect('profile')
    elif Client.objects.filter(user=user).exists():
        client = Client.objects.get(user=user)   
        if request.method=='POST':
            username = request.POST['username']

            client.nom = request.POST['nom']
            client.prenom = request.POST['prenom']
            client.adresse = request.POST['adresse']
            email = request.POST['email']
            if  user.username != request.POST['username']:
                if ( User.objects.filter(username=request.POST['username'].lower()).exists() or User.objects.filter(email=request.POST['email'].upper()).exists()) :
                    messages.success(request,'Username deja utilisé')   
                    return redirect('profile')


            if client.email != request.POST['email'].upper() and client.email != request.POST['email'].lower():    
                if (Client.objects.filter(email=request.POST['email'].lower()).exists() or Client.objects.filter(email=request.POST['email'].upper()).exists() or Employe.objects.filter(email=request.POST['email'].lower()).exists() or Employe.objects.filter(email=request.POST['email'].upper()).exists()) and client.email != request.POST['email'].lower() :
                    messages.success(request,'Email deja utilisé')   
                    return redirect('profile')
           

            client.email = email
            user.username = username  
            if 'image' in request.FILES:
                if checkfile(request.FILES['image']):
                    client.image = request.FILES['image']
                    client.is_image = True    
                else:
                    messages.success(request,'veuillez choisir une image valide')
                    redirect('profile')  
            user.save() 
            client.save()
            messages.success(request,'le profile a été modifié avec succés')
            return redirect('profile')
        else:
            return redirect('profile')    
    else:
        return redirect('profile')    
    






@login_required(login_url='login')
def reclamation(request):
    reclamations=Reclamation.objects.all()
    user=request.user
    if Employe.objects.filter(user=user).exists():
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/reclamation.html',{'reclamations':reclamations,'employee':employee,'user_type':'Employe'})
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/reclamation.html',{'reclamations':reclamations,'client':client,'user_type':'Client'})
    


@login_required(login_url='login')
def fairereclamation(request):
    if request.method == 'POST':
        sujet = request.POST['sujet']
        description = request.POST['description']
        user = request.user
        employee = Employe.objects.get(user=user)
        
        # Create the Reclamation object
        reclamation = Reclamation.objects.create(sujet=sujet, description=description, employe=employee)
        
        # Notify all Responsible RHs about the new Reclamation
        responsablerhs = ResponsableRH.objects.all()
        for responsablerh in responsablerhs:
            Notification.objects.create(
                user=responsablerh.employe.user,
                message=f"une nouvelle réclamation ( '{sujet}' ) a été ajouté par  {employee.user.username}.",
                link  = "reclamation")
             
        
        return redirect('reclamation')
    else:
        return redirect('reclamation')
    
 


  



@login_required(login_url='login')
def repondrereclamation(request, reclamationid):
    print("xxxxxxxxxx")
    if request.method=='POST':
        reclamation=Reclamation.objects.get(id=reclamationid)
        reponse = request.POST['reponse'].strip()  # Get the form input for the reponse field
        if reponse:  # If the input is not empty, update the reponse field
            reclamation.reponse = reponse
        else:  # If the input is empty, set a different default value
            reclamation.reponse = "Pas encore de réponse"

        reclamation.save()
        employe=reclamation.employe
        Notification.objects.create(
            user=employe.user,
            message=f"votre réclamation ( '{reclamation.sujet}' ) a été repondue par {request.user.username}.",
            link  = "reclamation")


        return redirect('reclamation')
    else:
        return redirect('reclamation')
    






    
@login_required(login_url='login')
def conge(request):
    user=request.user
    conges=Conge.objects.all()
    if  Employe.objects.filter(user=user).exists():
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/conge.html',{'employee':employee,'conges':conges,'user_type':'Employe'})
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/conge.html',{'client':client,'conges':conges,'user_type':'Client'})
    

@login_required(login_url='login')
def demanderconge(request):

    if request.method=='POST':
        raison=request.POST['raison']
        depart = request.POST.get('depart')
        fin = request.POST.get('fin')
        if depart > fin:
            messages.success(request,'la date de depart doit etre inferieur a la date de fin')
            return redirect('conge')
        user=request.user
        employee=Employe.objects.get(user=user)
        conge=Conge.objects.create(raison=raison,depart=depart,fin=fin,employe=employee)
        conge.save()
        # Notify all Responsible RHs about the new Reclamation
        responsablerhs = ResponsableRH.objects.all()
        for responsablerh in responsablerhs:
            Notification.objects.create(
                user=responsablerh.employe.user,
                message=f"{employee.user.username} a demandé un congé",
                link="conge",
              
            )
        return redirect('conge')
    else:
        return redirect('conge')  


@login_required(login_url='login')
def repondreconge(request, congeid):
    if request.method == 'POST':
        conge = Conge.objects.get(id=congeid)
        action = request.POST.get('action')

        if action == 'accept':
            conge.reponse = 'oui'
        else:
            conge.reponse = 'non'
        conge.save()  
        employe=conge.employe
        Notification.objects.create(
            user=employe.user,
            message=f"votre demande de congé a été répondue par {request.user.username}.",
            link  = "conge")  
        return redirect('conge')       
    else:
        return redirect('conge')            
            
            

       
@login_required(login_url='login')
def code(request):
    user=request.user
    codes = Code.objects.all().order_by('-date')
    #trie depending on date
   
    highlighted_codes=[[]]
    for code in codes:
        print(code.language)
        highlighted_codes.append(       [ highlight(code.fichier.read(), PythonLexer(), HtmlFormatter()  ) ,code.devlogiciel.employe.nom,  code.devlogiciel.employe.prenom,code.titre,code.language     ]             )
    if  Employe.objects.filter(user=user).exists():    
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/code.html',{'employee':employee,'highlighted_codes':highlighted_codes,'user_type':'Employe'})  
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/code.html',{'client':client,'highlighted_codes':highlighted_codes,'user_type':'Client'})     
  
@login_required(login_url='login')
def ajoutercode(request):

    if request.method=='POST':
        titre=request.POST['titre']
        fichier=request.FILES.get('file')
        check=0
        language=""
        if fichier:
            supported_extensions = ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp',
                            '.h', '.hpp', '.rb', '.php', '.swift', '.kt', '.ts', '.json',
                            '.xml', '.md', '.sh', '.bash', '.sql', '.yml', '.yaml', '.go', '.rs']
            supported_languages = ['python', 'javascript', 'html',  'css', 'java', 'c', 'cpp',
                            'c', 'cpp', 'ruby', 'php', 'swift', 'kotlin', 'typescript', 'json',
                            'xml', 'markdown', 'bash', 'bash', 'sql', 'yaml', 'yaml', 'go', 'rust']
            for extension in supported_extensions:
                if not fichier.name.endswith(extension):
                    check+=1
                else:
                    language=supported_languages[supported_extensions.index(extension)]
                    break
        if check==len(supported_extensions):
            messages.success(request,' seulement les fichiers suivants sont supportes : .py, .js, .html, .htm, .css, .java, .c, .cpp,.h, .hpp, .rb, .php, .swift, .kt, .ts, .json,.xml, .md, .sh, .bash, .sql, .yml, .yaml, .go, .rs')
            return redirect('code')
        if  fichier.size == 0:
            messages.success(request,'le fichier est vide')
            return redirect('code')
                      
        file_content = fichier.read()    
        user=request.user
        employee=Employe.objects.get(user=user)
        devlogicile=DevLogiciel.objects.get(employe=employee)
 
        code=Code.objects.create(titre=titre,fichier=fichier,devlogiciel=devlogicile,language=language)
        other_developpeur=DevLogiciel.objects.filter().exclude(employe=employee)
        for dev in other_developpeur:
            Notification.objects.create(
                user=dev.employe.user,
                message=f"{employee.nom} {employee.prenom} a ajouté un nouveau code à l'espace de développement",
                link="code",
              
            )
        code.save()
        return redirect('code')
    else:
        return redirect('code')  
    










@login_required(login_url='login') 
def stagiaire(request):
    user=request.user
    
    stagiaires=Stagiaire.objects.all()
    tachesaccomplies=0
    note=0
    infolist=[]
    for stagiaire in stagiaires:
        taches=Tache.objects.filter(stagiaire=stagiaire)
        for tache in taches:
            if tache.etat=="fait":
                tachesaccomplies+=1
            note+=int(tache.note)    
        infolist.append([stagiaire.employe.nom,stagiaire.employe.prenom,stagiaire.faculte,stagiaire.specialite,stagiaire.encadrant,len(taches),tachesaccomplies,note,stagiaire.id]) 
        tachesaccomplies=0
        note=0

    sorted_infolist = sorted(infolist, key=lambda x: x[7], reverse=True)
    if  Employe.objects.filter(user=user).exists():   
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/stagiare.html',{'employee':employee,'infolistofstagiaire':sorted_infolist,'user_type':'Employe' })
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/stagiare.html',{'client':client,'infolistofstagiaire':sorted_infolist,'user_type':'Client'})

from django.urls import reverse

@login_required(login_url='login')
def tache(request,pk):
    stagiaire=Stagiaire.objects.get(id=pk)
    taches=Tache.objects.filter(stagiaire=stagiaire)
    if request.method=='POST':
        titre=request.POST['titre']
        description=request.POST['description']
        tache=Tache.objects.create(titre=titre,description=description,stagiaire=stagiaire)
       

        Notification.objects.create(
            user=stagiaire.employe.user,
            message=f"vous avez une nouvelle tache de la part de votre encadrent {stagiaire.encadrant}",
            link=reverse('tache', kwargs={'pk': pk})
          
        )
        tache.save()
        return redirect('tache',pk=pk)
    else:

        return render(request,'dashboard/tache.html',{'stagiaire':stagiaire,'taches':taches,'user':request.user})

@login_required(login_url='login')
def fairetache(request,pk):
    tache=Tache.objects.get(id=pk)
  
    
    if request.method == 'POST':
        # Get the file from request.FILES
        fichier = request.FILES.get('file')

        # Check if a file was uploaded
        if fichier:
            # Save the file to the tache object
            tache.travail = fichier

        # Save the tache object to the database
        tache.save()
        
        Notification.objects.create (
            user=User.objects.get(username=tache.stagiaire.encadrant.strip()),
            message=f"votre stagiaire {tache.stagiaire.employe.nom} {tache.stagiaire.employe.prenom}  a soumis son travail à propos de la tache {tache.titre}",
            link=reverse('tache', kwargs={'pk': tache.stagiaire.id})
 
          
        )
     
        return redirect('tache',pk=tache.stagiaire.id)
    else:
        return redirect('tache',pk=tache.stagiaire.id)

@login_required(login_url='login')
def notertache(request,pk):
    tache=Tache.objects.get(id=pk)
    if request.method=='POST':
        input_note=request.POST['note']
        if int(input_note) not in range(0,11):
            messages.success(request,'la note doit etre entre 0 et 10')
            return redirect('tache',pk=tache.stagiaire.id)
        
        tache.note=input_note
        tache.etat="fait"
        tache.save()


        Notification.objects.create(
            user=tache.stagiaire.employe.user,
            message=f"votre encadrent {tache.stagiaire.encadrant} a vous a attribué {tache.note} / 10 à propos de la tache {tache.titre}",
            link=reverse('tache', kwargs={'pk': tache.stagiaire.id})
        )
       
        return redirect('tache',pk=tache.stagiaire.id)
    else:
        return redirect('tache',pk=tache.stagiaire.id)
@login_required(login_url='login')
def forum(request):
    user=request.user
    msgs=Message.objects.all().order_by('date')
    message_statuses = []
    for msg in msgs:
        if msg.sender.user == user:  # Compare message sender with current user
            message_statuses.append(True)
        else:
            message_statuses.append(False)
    if Employe.objects.filter(user=user).exists():   
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/forum.html',{'employe':employee,'user_type':'Employe','msgs': zip(msgs, message_statuses)})
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/forum.html',{'client':client,'user_type':'Client'})
    

@login_required(login_url='login')
def sendmsg(request):
    msgs=Message.objects.all().order_by('date')
  
            
    if request.method=='POST':
        user=request.user
        employe=Employe.objects.get(user=user)
        msg=request.POST['msg']
        message=Message.objects.create(message=msg,sender=employe)
        message.save()
    return redirect('forum')









@login_required(login_url='login')
def souscription(request):
    user=request.user
    if  Employe.objects.filter(user=user).exists():   
        employee=Employe.objects.get(user=user)
        return render(request,'dashboard/souscription.html',{'employee':employee,'user_type':'Employe'})
    else:
        client=Client.objects.get(user=user)
        return render(request,'dashboard/souscription.html',{'client':client,'user_type':'Client'})
   



@login_required(login_url='login')
def automobile(request):
    if request.method=='POST':
        user=request.user
        client=Client.objects.get(user=user)
        marque=request.POST['marque']
        date=request.POST['date']
        usage=request.POST['usage']
        new_assurance_car=AssuranceAutomobile.objects.create(marque=marque,date_premiercirculation=date,usage=usage,client=client)
        new_assurance_car.save()
        gestclients=GestionnaireServiceClient.objects.filter()
        for gestclient in gestclients:
            Notification.objects.create(
                user=gestclient.employe.user,
                message=f"le client {client.user.username} a demandé une assurance automobile",
                link="automobile",
            )

        return redirect('automobile')
    else:
        automobile=AssuranceAutomobile.objects.all()
        return render(request,'dashboard/automobile.html',{'automobile':automobile})


@login_required(login_url='login')
def repautomobile(request,automobileid):
    automobile=AssuranceAutomobile.objects.get(id=automobileid)
    if request.method=='POST':
        action = request.POST.get('action')
        if action == 'accept':
            automobile.reponse="ok"
        else:
            automobile.reponse="non"
        Notification.objects.create(
            user=automobile.client.user,
            message=f"votre demande d'assurance automobile a été répondue par le gestionnaire de service client {request.user.employe.nom} {request.user.employe.prenom}", 
            link="automobile",)   
        automobile.save()
        return redirect('automobile')    

    else:
        return render(request,'dashboard/repautomobile.html',{'automobile':automobile})
    


@login_required(login_url='login')
def habitation(request):
    if request.method=='POST':
        user=request.user
        client=Client.objects.get(user=user)
        superficie=request.POST['superficie']
        type=request.POST['type']
        new_habitat=AssuranceHabitation.objects.create(superficie=superficie,type=type,client=client)
        new_habitat.save()
        gestclients=GestionnaireServiceClient.objects.filter()
        for gestclient in gestclients:
            Notification.objects.create(
                user=gestclient.employe.user,
                message=f"le client {client.user.username} a demandé une assurance habitation",
                link="habitation",
            )
        return redirect('habitation')
    else:
        habitation=AssuranceHabitation.objects.all()
        return render(request,'dashboard/habitation.html',{'habitations':habitation})
    

@login_required(login_url='login')
def rephabitation(request,habitationid):
    habitation=AssuranceHabitation.objects.get(id=habitationid)
    if request.method=='POST':
        action = request.POST.get('action')
        if action == 'accept':
            habitation.reponse="ok"
        else:
            habitation.reponse="non"
        habitation.save()
        Notification.objects.create(
            user=habitation.client.user,
            message=f"votre demande d'assurance habitation a été répondue par le gestionnaire de service client {request.user.employe.nom} {request.user.employe.prenom}",
            link="habitation",)
        return redirect('habitation')    

    else:
        return render(request,'dashboard/rephabitation.html',{'habitation':habitation})    
    


def resetpassword(request):
    return render(request,'password_reset/resetpassword.html')    



from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist


def sendverificationmail(request):
    email = request.POST['email']
    try:
        employe = Employe.objects.get(email=email)
        user = employe.user
    except ObjectDoesNotExist:
        try:
            client = Client.objects.get(email=email)
            user = client.user
        except ObjectDoesNotExist:
            messages.error(request, 'Cet email n\'existe pas')
            return redirect('resetpassword')

 

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    protocol = 'http' 

    # Use the current site's domain to build the reset link
    reset_link = f'{protocol}://{current_site.domain}/reset-password/{uid}/{token}/'

    subject = 'Reset Password'
    message = render_to_string('password_reset/password_reset_email.html', {
       'reset_link': reset_link,
        'domain': current_site.domain,
        'username': user.username,
    })
  
    
    send_mail(subject, message, 'maeproductionzone@gmail.com', [email],   html_message=message )
    messages.success(request, 'Un email de verification vous a été envoyé')
    return render(request,'password_reset/resetpassword.html')   




from django.contrib.auth.forms import SetPasswordForm
def reset_password_click(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Handle invalid user id or token
        messages.error(request, 'Le lien a été expirée ou invalide')
        return redirect('password_reset_invalid')

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'votre mot de passe a été modifiée avec succées.')
                return redirect('password_reset_success')
        else:
            form = SetPasswordForm(user)

        return render(request, 'password_reset/password_reset_form.html', {'form': form})

    # Handle invalid token or link expired
    messages.error(request, 'Le lien a été expirée ou invalide.')
    return redirect('password_reset_invalid')

 


def password_reset_success(request):
    return render(request, 'password_reset/password_reset_success.html')

# views.py

def password_reset_invalid(request):
    return render(request, 'password_reset/password_reset_invalid.html')
