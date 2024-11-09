from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone
from django.urls import reverse, reverse_lazy


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

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices= NOTIFY, default="info")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}--{self.message}"


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifications = models.ForeignKey(Notifications, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=250, null=True, blank=False)
    last_name = models.CharField(max_length=250, null=True, blank=False)
    location = models.CharField(max_length=250, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    phone_number = models.CharField(max_length=250, null=True)
    message = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return f"{self.id} - {self.phone_number}"
    
    def get_absolute_url(self):
        return reverse('contact-detail', kwargs={ "pk":self.id})
    
    class Meta:
        ordering = ['-created_at']

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifications = models.ForeignKey(Notifications, on_delete=models.PROTECT, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.message} - {self.user.username}"

    def get_absolute_url(self):
        return reverse('user_dashboard', kwargs={"pk":self.user.id})

    class Meta:
        ordering =['sent_at']

class Subscription(models.Model):
    email = models.EmailField(null=True, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.email}"


def create_notification(sender, instance, created, **kwargs):
    if created:
        notification_message = ""
        if sender == Contact:
            notification_message = f"{instance.user.username} added a new contact: {instance.phone_number}"
        elif sender == Subscription:
            notification_message = f"You have successfully subscribed"
        elif sender == Feedback:
            notification_message = f"{instance.user.username} sent feedback"

        Notifications.objects.create(
            message=notification_message,
            created_at=timezone.now(),
            seen=False
        )

# Connecting the function to post_save signal for each model
post_save.connect(create_notification, sender=Contact)
post_save.connect(create_notification, sender=Subscription)
post_save.connect(create_notification, sender=Feedback)
        