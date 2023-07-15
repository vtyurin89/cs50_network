from random import choice
from re import search
from string import ascii_letters
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


def create_username_slug(translated_username):
    username_slug = slugify(translated_username)
    slug_check = User.objects.filter(slug=username_slug)
    if slug_check.exists():
        username_slug = f"{username_slug}_{choice(ascii_letters)}{choice(ascii_letters)}" \
                   f"{choice(ascii_letters)}{choice(ascii_letters)}"
    return username_slug


class User(AbstractUser):
    image = models.URLField(null=True, blank=True, verbose_name='Profile image')
    slug = models.SlugField(max_length=300, db_index=True, unique=True, verbose_name='URL part (slug)')
    birthday = models.DateField(blank=True, null=True)
    hobbies = models.CharField(blank=True, null=True, max_length=250)

    def cyrillic_letters_found(self):
        return bool(search('[а-яА-Я]', self.username))

    def cyrillic_letters_translate(self):
        translated_username = self.username.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
        return translated_username

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.cyrillic_letters_found():
                translated_username = self.username.cyrillic_letters_translate()
                self.slug = create_username_slug(translated_username)
            else:
                self.slug = create_username_slug(self.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_page_view', kwargs={'user_slug': self.slug})


class Post(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='authors')
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    liked = models.ManyToManyField('User', blank=True, related_name='liked_post')


class Follow(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, related_name='is_followed_by')
    follower = models.ForeignKey('User', on_delete=models.PROTECT, related_name='is_following')

    def __str__(self):
        return f'{self.follower} follows {self.user}'