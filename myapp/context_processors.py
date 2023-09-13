from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User, auth
from .models import Employe,Stagiaire,ResponsableRH,DevLogiciel,GestionnaireServiceClient,Encadrant,Client,Reclamation,Conge,Code,Tache,AssuranceAutomobile,AssuranceHabitation,Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def base(request):
    if request.user.is_authenticated:
        number_unseen_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
        for notif in Notification.objects.filter(user=request.user, is_read=False):
            notif.is_read = True
            notif.save()
    else:
        number_unseen_notifications = 0


    return {'number_unseen_notifications': number_unseen_notifications}




def acceptuser(request):
    users = User.objects.all()  # Assign the queryset directly here

    for user in users:
        if Employe.objects.filter(user=user).exists():
            employe = Employe.objects.get(user=user)
            if employe.etat and employe.nb_accepte == 0:
                employe.nb_accepte = 10
                employe.save()
                Notification.objects.create(
                    user=user,
                    message="votre membership a été bien accepté par l'administarteur",
                    link="www.geekhelmi.me/"
                )
        elif Client.objects.filter(user=user).exists():
            client = Client.objects.get(user=user)
            if client.etat and client.nb_accepte == 0:
                client.nb_accepte = 10
                client.save()
                Notification.objects.create(
                    user=user,
                    message="votre membership a été bien accepté par l'administarteur",
                    link="www.geekhelmi.me/"
                )

    return {'users': users}

        

 
