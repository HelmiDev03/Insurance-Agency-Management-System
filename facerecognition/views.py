from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import is_ajax, classify_face
import base64
from .models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User,auth
from myapp.models import Employe,Client
from django.contrib import messages
from myapp.views import faceid









def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        
        _, str_img = photo.split(';base64')

        # print(image)
        decoded_file = base64.b64decode(str_img)
 

        x = Log()
        x.image.save('image.png', ContentFile(decoded_file))
        x.save()

        res = classify_face(x.image.path)
        if res:
           
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                print("user founded")
                user = User.objects.get(username=res)
                if Client.objects.filter(user=user).exists():
                    client_in = Client.objects.filter(user=user)
                    x.client = client_in
                    x.save()
                elif Employe.objects.filter(user=user).exists():
                    employe_instance = Employe.objects.get(user=user)  # Get a single Employe instance
                    x.employe = employe_instance
                    x.save()  

                auth.login(request,user)    
            
                return render(request, 'dashboard/index.html', {'user': user})
            else:
                print("user not founded")
                messages.success(request,'visage non reconnu')
                return render(request, 'login/login.html', )
        else:
            return render(request, 'login/login.html', )