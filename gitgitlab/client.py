"""Interface to Gitlab and Git."""

import re

from gitlab import Gitlab
from git import Repo


class GitlabException(Exception):

    """Gitlab error."""

    pass


class NotFound(Exception):

    """The item looked for was not found."""

    pass


class GitlabClient(object):

    """Simple Gitlab client."""

    def __init__(self, url='https://gitlab.com'):
        """Initialize the Gitlab client.

        :param url: Base URL of the Gitlab server (https://gitlab.com by default)

        """
        self._url = url
        self._gitlab = None

    def login(self, token):
        """Login to Gitlab.

        :param token: The user's Gitlab private token.

        """
        self._gitlab = Gitlab(self._url, token)

    def get_projects(self):
        """Fetch the projects owned by the user.

        :return list: of projects.

        """
        return self._gitlab.owned_projects(per_page=1000)

    def get_project(self, name=None):
        """Return the project with the given name.

        :param name: Name of the project to return.
        :raise NotFound: if the project does not exist.

        """
        if not name:
            name = self.get_project_name()
        projects = self.get_projects()
        for p in projects:
            if p.name == name:
                return p
        raise NotFound(name)

    def create_project(self, name, wiki_enabled=False, public=False):
        """Create a project.

        :param name: Name of the project.
        :param wiki_enabled: Enable the wiki for this project.
        :param public: Make the project public.

        :return dict: with the created project

        """
        try:
            self.get_project(name)
        except NotFound:
            pass
        else:
            raise GitlabException("Project {0} already exists.".format(name))
        project = self._gitlab.Project({'name': name, 'wiki_enabled': wiki_enabled,
                                       'public': public})
        project.save()
        return project

    def track(self, project_name='gitlab', branch='master',
              remote_name='gitlab', no_push=False):
        """Set a gitlab repository as remote for the current git checkout.

        :return: The gitlab git remote.

        """
        project = self.get_project(project_name)
        repo = Repo('.')
        if not remote_name:
            raise GitlabException('Invalid remote name {0}'.format(remote_name))
        try:
            self.get_remote(remote_name)
        except NotFound:
            pass
        else:
            raise GitlabException('Remote name {0} already exists.'.format(remote_name))
        remote = repo.create_remote(remote_name, project.ssh_url_to_repo)
        remote.push(branch, set_upstream=True)
        return remote

    def get_gitlab_remote(self):
        """Return the gitlab remote of the repository in the current directory.

        :raise NotFound: if the gitlab remote is not found.

        """
        return self.get_remote('gitlab')

    def get_remote(self, name):
        """Return the remote with the given name of the repository in the current directory."""
        repo = Repo('.')
        if not hasattr(repo, 'remotes'):
            raise NotFound()
        for remote in repo.remotes:
            if remote.name == name:
                return remote
        raise NotFound()

    def get_project_name(self):
        """Return the name of the gitlab project that is tracking the repository in the current directory."""
        remote = self.get_gitlab_remote()
        return self.get_project_name_from_url(remote.url)

    @staticmethod
    def get_project_name_from_url(url):
        return re.search(r'/(\S+).git', url).groups()[0]

    def get_project_page(self, name=None):
        """Return the url of the page of a Gitlab project.

        :param name: Name of the project. If not provided, it will use the project name
            tracking the repository in the current directory.
        :return: Gitlab project page url.

        """
        project = self.get_project(name)
        url = project.http_url_to_repo
        if url.endswith('.git'):
            url = url[:-4]
        return url
