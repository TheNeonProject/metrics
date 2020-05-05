from django.db import models
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    started_at = models.DateField()
    finished_at = models.DateField(blank=True, null=True)
    jira_codename = models.CharField(max_length=100)
    github_repository = models.CharField(max_length=100)
