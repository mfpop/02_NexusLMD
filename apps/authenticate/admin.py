from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Profile, WorkExperience


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Personal Info', {
            'fields': ('title', 'phone', 'bio', 'avatar_data')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date_created', 'date_modified')


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0
    fields = ('company', 'position', 'start_date', 'end_date')
    readonly_fields = ('date_created', 'date_modified')


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, WorkExperienceInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_status')
    
    def profile_status(self, obj):
        if hasattr(obj, 'profile'):
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    
    profile_status.short_description = 'Profile Created'


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email', 'company', 'position')
    list_filter = ('start_date', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('user', 'company', 'position')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Details', {
            'fields': ('description',)
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'country', 'date_created')
    search_fields = ('user__username', 'user__email', 'title', 'city', 'country')
    list_filter = ('date_created', 'country')
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (None, {
            'fields': ('user', 'title')
        }),
        ('Personal Info', {
            'fields': ('phone', 'bio', 'avatar_data')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_modified')
        }),
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)