from django.contrib import admin
from second_day.models import SelfIntroduction,Favorite

# Register your models here.

#define a model-management class
class SelfIntroductionAdmin(admin.ModelAdmin):
    msg_display = ['id','name']

class FavoriteAdmin(admin.ModelAdmin):
    msg_display = ["item","whos_favorite"]

admin.site.register(SelfIntroduction,SelfIntroductionAdmin)

admin.site.register(Favorite,FavoriteAdmin)
        



