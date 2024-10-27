from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse, reverse_lazy




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


IDENTITY = (
    ('ghana card','Ghana Card'),
    ('drivers license','Drivers License'),
    ('international passport','International Passport'),
    ('none','None')
)


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=False, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER, default="other")
    otp = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices= NOTIFY, default="info")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}--{self.message}"


class Profile(models.Model):
    image = models.FileField(upload_to =user_image_directory)
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    notifications = models.ForeignKey(Notifications, on_delete=models.PROTECT, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True, choices=GENDER, default="other")
    phone = models.CharField(max_length= 20, null=True, blank=True)
    country = models.CharField(max_length= 120, null=True, blank=True)
    state = models.CharField(max_length= 200, null=True, blank=True)
    address = models.CharField(max_length= 2000, null=True, blank=True)
    identity_type = models.CharField(max_length=200, null=True, blank=True, choices=IDENTITY, default="none")
    identity_card = models.FileField(upload_to='user_image_directory')
    facebook = models.CharField(max_length= 100, null=True, blank=True)
    twitter = models.CharField(max_length= 100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        if self.full_name:
            return self.full_name
        else:
            return self.user.username
    
    class Meta:
        ordering =['-date']

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notifications = models.ForeignKey(Notifications, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"






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


class LetsVibe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True, null = True)
    notifications = models.ForeignKey(Notifications, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.message



class FAQs(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    notifications = models.ForeignKey(Notifications, on_delete=models.PROTECT, null=True)
    question = models.TextField(null=True, blank=True)
    answer = models.CharField(max_length=200, null=True, blank=True)
    date_asked = models.DateTimeField(auto_now_add=True, null=True)
    date_answered = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}-- {self.question}"


class Subscription(models.Model):
    email = models.EmailField(null=True, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.email}"
    
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)



def create_notification(sender, instance, created, **kwargs):
    if created:
        notification_message = ""
        if sender == Profile:
            notification_message = f"{instance.user.username} added a profile: {instance.full_name}"
        elif sender == Todo:
            notification_message = f"{instance.user.username} added a todo: {instance.title}"
        
        elif sender == LetsVibe:
            notification_message = f"{instance.user.username} added a new message: {instance.message}"
        elif sender == Subscription:
            notification_message = f"{instance.user.username} subscribed"
        elif sender == Feedback:
            notification_message = f"{instance.user.username} sent feedback"

        Notifications.objects.create(
            user=instance.user, 
            message=notification_message,
            created_at=timezone.now(),
            seen=False
        )

# Connecting the function to post_save signal for each model
post_save.connect(create_notification, sender=Profile)
post_save.connect(create_notification, sender=Todo)
post_save.connect(create_notification, sender=LetsVibe)
post_save.connect(create_notification, sender=Subscription)
post_save.connect(create_notification, sender=Feedback)
