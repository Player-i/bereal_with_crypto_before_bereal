from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from PIL import Image

# Create your models here.

User = settings.AUTH_USER_MODEL

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	coins = models.DecimalField(default=0, decimal_places=3, max_digits=8)
	profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg', null=True, blank=True)
	followers = models.ManyToManyField(User, blank=True, related_name='_follow')
	following = models.ManyToManyField(User, blank=True, related_name='_following')
	dms = models.ManyToManyField(User, blank=True, verbose_name='dms')
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	caption = models.CharField(max_length=140)
	image = models.ImageField(upload_to='feed_images', null=True, blank=True, verbose_name='image')
	likes = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name='likes')
	question = models.CharField(max_length=50)
	option1 = models.CharField(max_length=50)
	option2 = models.CharField(max_length=50)
	option3 = models.CharField(max_length=50)
	correct_answer = models.CharField(max_length=50)
	users_did_quiz = models.ManyToManyField(User, default=None, blank=True, related_name="users_did_quiz")
	users_right = models.ManyToManyField(User, default=None, blank=True, related_name="users_right")

	def __str__(self):
		return self.caption

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)

	@property
	def total_likes(self):
		return self.likes.all().count()

	@property
	def total_comments(self):
		return self.comments.all()

class Coin(models.Model):
	network_coins = models.DecimalField(default=1000, decimal_places=3, max_digits=8)

	def __str__(self):
		network_coins = 'network coins'
		return network_coins

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
	body = models.TextField()


