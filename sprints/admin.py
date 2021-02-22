from django.conf import settings
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone

from .models import Sprint, SprintMember
from .services import SprintCloneService
from .tasks import analyze_sprint


def analyze_current_sprint(modeladmin, request, queryset):
    messages.success(request, 'Analyzing...')
    analyze_sprint.delay()
analyze_current_sprint.short_description = 'Analyze current sprint'


def generate_next_sprints(modeladmin, request, queryset):
    for sprint in queryset:
        SprintCloneService.clone_sprint(sprint)

generate_next_sprints.short_description = 'Generate sprints from selected'


class SprintMemberAdmin(admin.ModelAdmin):
    pass


class SprintAdmin(admin.ModelAdmin):
    actions = [analyze_current_sprint, generate_next_sprints]
    list_display = (
        'project',
        'number_team_members', 'member_names',
        'started_at', 'number_weeks', 'finished_at',
        'stories_done',
        'percentage_stories_done_bar',
        'number_releases', 'last_release'
    )
    list_filter = ('started_at', 'project', 'members')

    def percentage_stories_done_bar(self, obj):
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            obj.percentage_stories_done
        )


admin.site.register(Sprint, SprintAdmin)
admin.site.register(SprintMember, SprintMemberAdmin)
