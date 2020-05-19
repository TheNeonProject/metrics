from datetime import timedelta

from django.utils import timezone
from dateutil.parser import parse
import requests
from requests.auth import HTTPBasicAuth

from .models import Sprint


class SprintAnalysis():
    def __init__(self, config):
        self.github_token = config['github_token']
        self.jira_user = config['jira_user']
        self.jira_token = config['jira_token']

    def execute(self, projects):
        today = timezone.now().date()

        for project in projects:
            # In case we're on a planning day, we update the numbers
            # of the finishing sprint, the new sprint shouldn't have any numbers on it
            # probably the first day
            current_sprint = Sprint.objects.filter(
                project=project, started_at__lte=today, finished_at__gte=today
            ).order_by('started_at').first()

            if not current_sprint:
                current_sprint = Sprint.objects.create(
                    project=project,
                    started_at=today,
                    number_weeks=project.default_sprint_length_in_weeks,
                    finished_at=today + timedelta(
                        days=7 * project.default_sprint_length_in_weeks)
                )

            github = GithubService(self.github_token)
            jira = JiraService(self.jira_user, self.jira_token)

            current_sprint.last_release = github.get_latest_release_datetime(
                project.github_repository)
            current_sprint.number_releases = github.get_release_count(
                project.github_repository,
                current_sprint.started_at
            )
            current_sprint.total_stories = jira.get_total_stories(project.jira_codename)
            current_sprint.stories_done = jira.get_stories_done(project.jira_codename)
            current_sprint.total_bugs = jira.get_all_bugs(project.jira_codename)
            current_sprint.bugs_done = jira.get_bugs_done(project.jira_codename)
            current_sprint.tasks_done = jira.get_tasks_done(project.jira_codename)
            current_sprint.half_sprint_issues = jira.get_half_sprint_issues(project.jira_codename)
            current_sprint.save()


class JiraService:
    ENDPOINT = 'https://theneonproject.atlassian.net/rest/api/3/search'

    ALL_STORIES = 'project = {project} AND issuetype = Story AND sprint in openSprints()'
    ALL_BUGS = 'project = {project} AND issuetype = Bug AND sprint in openSprints()'
    STORIES_DONE = 'project = {project} AND issuetype = Story AND sprint in openSprints() AND Status = Done'
    BUGS_DONE = 'project = {project} AND issuetype = Bug AND sprint in openSprints() AND Status = Done'
    TASKS_DONE = 'project = {project} AND issuetype = Task AND sprint in openSprints() AND Status = Done'
    HALF_SPRINT_ISSUES = "project = {project} AND sprint in openSprints() AND labels = 'unplanned'"

    def __init__(self, user, token):
        self.user = user
        self.token = token

    def get_half_sprint_issues(self, project_name):
        return self.perform_query_for_total(
            project_name, self.HALF_SPRINT_ISSUES)

    def get_stories_done(self, project_name):
        return self.perform_query_for_total(project_name, self.STORIES_DONE)

    def get_bugs_done(self, project_name):
        return self.perform_query_for_total(project_name, self.BUGS_DONE)

    def get_tasks_done(self, project_name):
        return self.perform_query_for_total(project_name, self.TASKS_DONE)

    def get_all_bugs(self, project_name):
        return self.perform_query_for_total(project_name, self.ALL_BUGS)

    def get_total_stories(self, project_name):
        return self.perform_query_for_total(project_name, self.ALL_STORIES)

    def perform_query_for_total(self, project_name, query):
        content = requests.post(
            self.ENDPOINT,
            auth=HTTPBasicAuth(self.user, self.token),
            json={'jql': query.format(project=project_name)})
        return content.json()['total']


class GithubService:
    GH_LATEST_RELEASE_ENDPOINT = 'https://api.github.com/repos/TheNeonProject/{project_name}/releases/latest'
    GH_LIST_RELEASES_ENDPOINT = 'https://api.github.com/repos/TheNeonProject/{project_name}/releases'

    def __init__(self, token):
        self.token = token

    def get_latest_release_datetime(self, project_name):
        content = requests.get(
            self.GH_LATEST_RELEASE_ENDPOINT.format(project_name=project_name),
            headers={'Authorization': f'Token {self.token}'})

        try:
            created_at = parse(content.json()['created_at'])
        except KeyError:
            return ''

        return created_at

    def get_release_count(self, project_name, started_sprint_date):
        release_count = 0

        content = requests.get(
            self.GH_LIST_RELEASES_ENDPOINT.format(project_name=project_name),
            headers={'Authorization': f'Token {self.token}'})

        for item in content.json():
            try:
                created_at_release = parse(item['created_at'])
            except (KeyError, TypeError):
                return 0

            if created_at_release.date() >= started_sprint_date:
                release_count += 1
            else:
                break

        return release_count
