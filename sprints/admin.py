from django.contrib import admin

from django.contrib import admin

from .models import Sprint


class SprintAdmin(admin.ModelAdmin):
    list_display = (
        'started_at', 'number_weeks', 'finished_at', 'percentage_stories_done'
    )


admin.site.register(Sprint, SprintAdmin)
