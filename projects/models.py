from django.db import models
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    started_at = models.DateField()
    finished_at = models.DateField(blank=True, null=True)
    jira_codename = models.CharField(max_length=100)
    github_repository = models.CharField(max_length=100)
    default_sprint_length_in_weeks = models.IntegerField(default=2)
    number_team_members = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name}'
