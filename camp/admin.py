from django.contrib import admin
from .models import Collective, MembersOfCollective, User

admin.site.register(Collective)
admin.site.register(MembersOfCollective)
admin.site.register(User)
