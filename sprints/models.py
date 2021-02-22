import math

from django.db import models
from model_utils.models import TimeStampedModel

from projects.models import Project


class SprintMember(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name}'


class Sprint(TimeStampedModel):
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.PROTECT)
    started_at = models.DateField()
    number_weeks = models.IntegerField(default=1)
    finished_at = models.DateField()
    total_stories = models.IntegerField(default=0, blank=True, null=True)
    stories_done = models.IntegerField(default=0, blank=True, null=True)
    total_bugs = models.IntegerField(default=0, blank=True, null=True)
    bugs_done = models.IntegerField(default=0, blank=True, null=True)
    tasks_done = models.IntegerField(default=0, blank=True, null=True)
    half_sprint_issues = models.IntegerField(default=0, blank=True, null=True)
    last_release = models.DateField(null=True, blank=True)
    number_releases = models.IntegerField(default=0, blank=True, null=True)
    members = models.ManyToManyField(SprintMember)

    @property
    def number_team_members(self):
        return self.members.count()

    @property
    def member_names(self):
        return ', '.join([member.name for member in self.members.all()])

    @property
    def percentage_stories_done(self):
        if self.total_stories == 0:
            return 0
        return math.trunc((self.stories_done / self.total_stories) * 100)

    def __str__(self):
        return f'{self.project} sprint started {self.started_at}'
