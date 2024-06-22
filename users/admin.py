from django.contrib import admin
from .models import CustomUser,Post,Subscription,Block

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Subscription)
admin.site.register(Block)