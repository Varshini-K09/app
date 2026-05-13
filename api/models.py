from django.db import models
from .validators import validate_email, validate_password, validate_phone_number
# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True, validators=[validate_email])
    password=models.CharField(max_length=100, validators=[validate_password])

    def __str__ (self):
        return self.name
    
class Profile(BaseModel):

    full_name = models.CharField(max_length=100, blank=True)

    bio = models.TextField(blank=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number]
    )

    address = models.TextField(blank=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return self.user.name