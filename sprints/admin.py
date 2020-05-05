from django.contrib import admin
from django.utils.html import format_html

from .models import Sprint


class SprintAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'started_at', 'number_weeks', 'finished_at',
        'total_stories', 'stories_done',
        'percentage_stories_done_bar',
        'half_sprint_issues',
        'total_bugs',
        'bugs_done', 'last_release'
    )
    list_filter = ('started_at', 'project')

    def percentage_stories_done_bar(self, obj):
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            obj.percentage_stories_done
        )


admin.site.register(Sprint, SprintAdmin)
