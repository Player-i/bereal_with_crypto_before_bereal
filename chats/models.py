from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from PIL import Image

# Create your models here.

User = settings.AUTH_USER_MODEL

class Message(models.Model):
	author = models.ForeignKey(User, null=True, related_name='message_author', on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, null=True, related_name='receiver', on_delete=models.CASCADE)
	content = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username