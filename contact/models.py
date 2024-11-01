from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def user_image_directory(instance, filename, folder):
    ext = filename.split('.')[-1]
    filename = f"{instance.user.id}.{ext}"
    return f"user_{instance.user.id}/{folder}/{filename}"

def user_image_path(instance, filename):
    return user_image_directory(instance, filename, 'images')

def identity_card_path(instance, filename):
    return user_image_directory(instance, filename, 'identity_cards')

GENDER = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other')
)


NOTIFY = (
    ('warning','warning'),
    ('error','error'),
    ('info','info')
)




class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=False, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER, default="other")
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, null=True, blank=False)
    last_name = models.CharField(max_length=250, null=True, blank=False)
    location = models.CharField(max_length=250, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    phone_number = models.CharField(max_length=250, null=True)
    message = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return f"{self.contact_id} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('contact-detail', kwargs={ "pk":self.contact_id})
    
    class Meta:
        ordering = ['-created_at']
        