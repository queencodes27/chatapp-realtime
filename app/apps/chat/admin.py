from django.contrib import admin

from .models import Chat, Group, GroupMessage, UserMessage

admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(UserMessage)
