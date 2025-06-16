from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blogs",
    )
    title = models.TextField(max_length=100)
    blog = models.TextField(max_length=5000)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    url_link = models.CharField(max_length=200)
    url_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True)
    # avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(max_length=100, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    created_at = models.DateField(auto_now_add=False)

    def last_login(self):
        return self.user.last_login
    
    def username(self):
        return self.user.username
    
    def email(self):
        return self.user.email
    
    def __str__(self):
        return self.user.username
