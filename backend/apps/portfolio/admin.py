from django.contrib import admin
from .models import Profile, Skill, Project, Education, Experience


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'location', 'open_to_work', 'updated_at']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'tagline', 'bio', 'avatar', 'resume')}),
        ('Contact', {'fields': ('email', 'phone', 'location')}),
        ('Social Links', {'fields': ('github', 'linkedin', 'twitter', 'website')}),
        ('Status', {'fields': ('years_experience', 'open_to_work')}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order', 'is_visible']
    list_filter = ['category', 'is_visible']
    list_editable = ['order', 'is_visible', 'proficiency']
    search_fields = ['name']
    ordering = ['category', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_featured']
    list_editable = ['is_featured', 'order']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-is_featured', 'order']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_year', 'end_year', 'is_current', 'order']
    list_editable = ['order']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'employment_type', 'start_date', 'end_date', 'is_current', 'order']
    list_editable = ['order']
