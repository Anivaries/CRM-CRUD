from django.contrib import admin
from .models import Agent, Lead, User, UserProfile, Category

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)