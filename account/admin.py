from django.contrib import admin
from .models import Profile,UserPost,Department
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
# Register your models here.
class UserPostAdmin(admin.ModelAdmin):
    list_display = ['name','active','order']
admin.site.register(UserPost,UserPostAdmin)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','active','order']
admin.site.register(Department,DepartmentAdmin)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = '详细信息'
class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserProfileAdmin)
#AdminSite.logout_template='registration/logged_out.html'
