from django.contrib import admin
from .models import diary_emotion
# Register your models here.

from .models import diary_image

class diary_imageAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    search_fields = ['username']

admin.site.register(diary_image, diary_imageAdmin)

# Register your models here.
admin.site.register(diary_emotion)