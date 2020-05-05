from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = (
        'name', 'jira_codename', 'github_repository',
        'started_at', 'finished_at'
    )


admin.site.register(Project, ProjectAdmin)
