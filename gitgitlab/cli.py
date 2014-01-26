"""CLI interface for GitGitlab."""

import sys

from opster import command, dispatch
import webbrowser

from gitgitlab.auth import get_token
from gitgitlab.client import GitlabClient


def get_gitlab():
    """Return a logged-in instance of the gitlab client."""
    gitlab = GitlabClient()
    gitlab.login(get_token())
    return gitlab


def git():
    """Git entry point."""
    try:
        dispatch()
    except Exception, e:
        raise
        sys.exit(e)


@command()
def list():
    """List the projects owned by the user."""
    gitlab = get_gitlab()
    for p in gitlab.get_projects():
        print ': '.join([p.name, p.ssh_url_to_repo])


@command()
def open(project_name=None):
    """Open the project page in the default web browser."""
    gitlab = get_gitlab()
    url = gitlab.get_project_page(project_name)
    print 'Open {0}'.format(url)
    webbrowser.open(url)


@command()
def track(project_name, branch='master',
          remote=('r', 'gitlab', 'Name to give to the Gitlab remote'),
          no_push=('n', False, 'Do not push and do not set your Gitlab project as remote')):
    """Set a gitlab project as remote source."""
    gitlab = get_gitlab()
    gitlab.track(project_name, remote_name=remote, branch=branch, no_push=no_push)


@command()
def create(project_name,
           wiki=('w', False, 'Enable the wiki for the new project'),
           public=('p', False, 'Make the project public'),
           track=('t', False, 'Set this gitlab project as remote (requires push)'),
           branch=('b', 'master', 'Branch this project should track'),
           remote=('r', 'gitlab', 'Name to give to the Gitlab remote')):
    """Create a Gitlab project and add it as remote."""
    gitlab = get_gitlab()
    project = gitlab.create_project(project_name, wiki_enabled=wiki, public=public)
    print 'Project {0} created on Gitlab: {1}'.format(project.name, gitlab.get_project_page(project.name))
    if track:
        r = gitlab.track(project_name, remote_name=remote, branch=branch)
        print 'New remote {0}: {1}'.format(remote, r.url)
