from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True,default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True,)
    email = models.EmailField(max_length=50,unique=True,)
    country = models.CharField(max_length= 50,default="")
    phone_number = models.CharField(max_length=50,default="",verbose_name='Phone Number')
    def __str__(self):
        return f"{self.profile_image.url if self.profile_image else 'No image'} : {self.first_name} {self.last_name} {self.username} {self.email} {self.phone_number}"

class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False, related_name="message_sender")
    recipient = models.ForeignKey(User,on_delete= models.CASCADE,blank=False,null=False,related_name="message_recipient")
    message = models.TextField(max_length = 500)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.sender}: {self.recipient} {self.message} {self.date}"
    
class Chat(models.Model):
    participants = models.ManyToManyField(User,related_name="chats")
    messages = models.ManyToManyField(Message,blank=True,related_name="chats_messages")
    created_ar= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Chat{self.id} ({','.join(str[user] for user in self.participants.all())})"

class Post(models.Model):
    post = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userPost')
    like = models.IntegerField(default=0,  validators=[MinValueValidator(0)])
    def __str__(self):
        return f"{self.user}: {self.post}   {self.date}"
    
class Followers(models.Model):
    userFollowed = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userFollowed');
    userWhoFollows = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userWhoFollows');
    def __str__(self):
        return f"{self.userFollowed}: {self.userWhoFollows}"
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name='userLike');
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,null=False,related_name='postLike');
    def __str__(self):
        return f"{self.user}: {self.post}"
