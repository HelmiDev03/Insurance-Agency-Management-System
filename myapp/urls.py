
from . import  views
from django.urls import path










urlpatterns=[
  
  path('', views.login, name='login'),
  path("home/", views.home, name="home"),
  path('signup/', views.employeeclient, name='signup'),
  path('login/', views.login, name='login'),
  path('faceid/', views.faceid, name='faceid'),
  path('signupemploye/', views.signupemploye, name='signupemploye'),
  path('signupclient/', views.signupclient, name='signupclient'),
  path('signupstagiaire/<int:employeeid>', views.signupstagiaire, name='signupstagiaire'),
  path('signupdevlogiciel/<int:employeeid>', views.signupdevlogiciel, name='signupdevlogiciel'),
  path('logout/', views.logout, name='logout'),
  path('profile/', views.profile, name='profile'),
  path('profileupdate/', views.profileupdate, name='profileupdate'),
  path('reclamation/', views.reclamation, name='reclamation'),
  path('fairereclamation/', views.fairereclamation, name='fairereclamation'),
  path('repondrereclamation/<int:reclamationid>/', views.repondrereclamation, name='repondrereclamation'),
  path('conge/', views.conge, name='conge'),
  path('demanderconge/', views.demanderconge, name='demanderconge'),
  path('repondreconge/<int:congeid>/', views.repondreconge, name='repondreconge'),
  path('code/', views.code, name='code'),
  path('ajoutercode/', views.ajoutercode, name='ajoutercode'),
  path('stagiaire/', views.stagiaire, name='stagiaire'),
  path('tache/<int:pk>', views.tache, name='tache'),
  path('fairetache/<int:pk>', views.fairetache, name='fairetache'),
  path('notertache/<int:pk>', views.notertache, name='notertache'),

    path(('forum/'), views.forum, name='forum'),
    path("sendmsg/", views.sendmsg, name="sendmsg"),

  path('souscription/', views.souscription, name='souscription'),
  path('automobile/', views.automobile, name='automobile'),
  path('repautomobile/<int:automobileid>/', views.repautomobile, name='repautomobile'),
  path('habitation/', views.habitation, name='habitation'),
  path('rephabitation/<int:habitationid>/', views.rephabitation, name='rephabitation'),
 path(' notifications/', views.notifications, name='notifications'),
 path('supprimer_notification/<int:pk>/', views.supprimer_notification, name='supprimer_notification'),


  path('resetpassword/', views.resetpassword, name='resetpassword'),
  path('sendverificationmail/', views.sendverificationmail, name='sendverificationmail'),
  path('reset-password/<str:uidb64>/<str:token>/', views.reset_password_click, name='reset_password_click'),

  path('reset-password/success/', views.password_reset_success, name='password_reset_success'),
  path('reset-password/invalid/', views.password_reset_invalid, name='password_reset_invalid'),

    ]






