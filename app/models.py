from django.db import models

# Create your models here.
class ContactMe(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return "{} | {}".format(self.name,self.email)

class Github(models.Model):
    project_name = models.CharField(max_length=500)
    image=models.ImageField(upload_to="uploads/app")
    link=models.CharField(max_length=100,default="null")
    demolink=models.CharField(max_length=100,default="null")
