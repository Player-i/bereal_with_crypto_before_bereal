# Generated by Django 4.0.2 on 2022-02-26 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('coins', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('profile_image', models.ImageField(blank=True, default='profile_images/default.jpg', null=True, upload_to='profile_images')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(blank=True, related_name='_follow', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='_following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_coins', models.DecimalField(decimal_places=3, default=1000, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=140)),
                ('image', models.ImageField(blank=True, null=True, upload_to='feed_images', verbose_name='image')),
                ('question', models.CharField(max_length=50)),
                ('option1', models.CharField(max_length=50)),
                ('option2', models.CharField(max_length=50)),
                ('option3', models.CharField(max_length=50)),
                ('correct_answer', models.CharField(max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='likes')),
                ('users_did_quiz', models.ManyToManyField(blank=True, default=None, related_name='users_did_quiz', to=settings.AUTH_USER_MODEL)),
                ('users_right', models.ManyToManyField(blank=True, default=None, related_name='users_right', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.post')),
            ],
        ),
    ]
