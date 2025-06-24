from django.contrib import admin
from .models import User,Task
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class SimpleUserAdmin(UserAdmin):
    list_display = ('username','email','role')
    fieldsets = ((None, {'fields': ('username','email','role','is_active')}),)
    add_fieldsets = ((None, {'fields': ('username','email','password1','password2','role')}),)


class TaskAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        if not obj.assigned_by_id:
            obj.assigned_by = request.user
        super().save_model(request,obj,form,change)

    def get_readonly_fields(self,request,obj=None):
        if obj:
            return ['assigned_by'] +list(super().get_readonly_fields(request,obj))
        return super().get_readonly_fields(request,obj)

    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == 'assigned_by':
            kwargs['queryset'] = User.objects.filter(role__in=['ADMIN','MANAGER'])
        return super().formfield_for_foreignkey(db_field,request,**kwargs)





admin.site.register(Task,TaskAdmin)
