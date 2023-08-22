from django.db import models

# Create your models here.
class  TodoUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class TODO(models.Model):
    status_choices = [
    ('C', 'COMPLETED'),
    ('P', 'PENDING'),
    ]
    priority_choices = [
    ('1', '1️⃣'),
    ('2', '2️⃣'),
    ('3', '3️⃣'),
    ('4', '4️⃣'),
    ('5', '5️⃣'),
    ('6', '6️⃣'),
    ('7', '7️⃣'),
    ('8', '8️⃣'),
    ('9', '9️⃣'),
    ('10', '🔟'),
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2 , choices=status_choices)
    user  = models.ForeignKey(TodoUser  , on_delete= models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=2 , choices=priority_choices)