from . import views

from django.urls import path



urlpatterns = [
    path('', views.find_user_view, name='classify'),
]