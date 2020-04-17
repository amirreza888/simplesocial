from django.contrib import admin
from .models import GroupMember,Group
# Register your models here.


admin.site.register(GroupMember)

class GroupMemberInline(admin.TabularInline):
    model = GroupMember

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    inlines = [
        GroupMemberInline,
    ]