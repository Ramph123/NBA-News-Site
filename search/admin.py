from django.contrib import admin

from .models import News, Team, Player

admin.site.register(News)
admin.site.register(Team)
admin.site.register(Player)