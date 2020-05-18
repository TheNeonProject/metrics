from django.conf import settings
from celery.decorators import task

from sprints.services import SprintAnalysis
from projects.models import Project


@task(name='analyze_sprint')
def analyze_sprint():
    config = {
        'github_token': settings.GITHUB_TOKEN,
        'jira_user': settings.JIRA_USER,
        'jira_token': settings.JIRA_TOKEN
    }
    projects = Project.objects.filter(finished_at__isnull=True)
    SprintAnalysis(config).execute(projects)
