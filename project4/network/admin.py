from django.contrib import admin
from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'slug')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)