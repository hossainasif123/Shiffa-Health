from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PUBLIC='public'
    DOCTOR='doctor'
    ADMIN='admin'
    
    ROLE_CHOICES=[
        (PUBLIC,'Public(patient)'),
        (DOCTOR,'Doctor'),
        (ADMIN,'Admin'),

    ]
    role= models.CharField(max_length=10,choices=ROLE_CHOICES,default=PUBLIC)
    email=models.EmailField(unique=True)
    
    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
   
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role=self.ADMIN
        super().save(*args, **kwargs)

        
        