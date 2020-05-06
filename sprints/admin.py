from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from projects.models import Project
from .models import Sprint
from .services import SprintAnalysis


def analyze_current_sprint(modeladmin, request, queryset):
    config = {
        'github_token': settings.GITHUB_TOKEN,
        'jira_user': settings.JIRA_USER,
        'jira_token': settings.JIRA_TOKEN
    }
    projects = Project.objects.filter(finished_at__isnull=True)
    SprintAnalysis(config).execute(projects)
analyze_current_sprint.short_description = 'Analyze current sprint'


class SprintAdmin(admin.ModelAdmin):
    actions = [analyze_current_sprint]
    list_display = (
        'project',
        'started_at', 'number_weeks', 'finished_at',
        'total_stories', 'stories_done',
        'percentage_stories_done_bar',
        'half_sprint_issues',
        'total_bugs',
        'bugs_done', 'tasks_done', 'number_releases', 'last_release'
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
