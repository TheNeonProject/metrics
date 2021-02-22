from django.conf import settings
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Sprint
from .tasks import analyze_sprint


def analyze_current_sprint(modeladmin, request, queryset):
    messages.success(request, 'Analyzing...')
    analyze_sprint.delay()
analyze_current_sprint.short_description = 'Analyze current sprint'


class SprintMemberInline(admin.TabularInline):
    model = Sprint.members.through


class SprintAdmin(admin.ModelAdmin):
    inlines = [SprintMemberInline]
    actions = [analyze_current_sprint]
    list_display = (
        'project',
        'number_team_members',
        'started_at', 'number_weeks', 'finished_at',
        'stories_done',
        'percentage_stories_done_bar',
        'number_releases', 'last_release'
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
