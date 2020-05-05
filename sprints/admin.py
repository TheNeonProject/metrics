from django.contrib import admin

from django.contrib import admin

from .models import Sprint


class SprintAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'started_at', 'number_weeks', 'finished_at',
        'total_stories', 'stories_done',
        'percentage_stories_done',
        'half_sprint_issues',
        'total_bugs',
        'bugs_done', 'last_release'
    )
    list_filter = ('started_at', 'project')


admin.site.register(Sprint, SprintAdmin)
