from django.db import models
from myapp.models import Employe,Client

# Create your models here.
class Log(models.Model):
    image=models.ImageField(upload_to='logspics/',null=True,blank=True)
    is_correct=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE,null=True,blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True,blank=True)