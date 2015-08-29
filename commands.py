import sublime_plugin
import sublime

import os
import time
from subprocess import call

class GitDirectoryCache(object):
    cache = {};

    @classmethod
    def is_git(cls, path):
        now = time.time()

        if path in GitDirectoryCache.cache:
            if GitDirectoryCache.cache[path]['timeout'] > now:
                return GitDirectoryCache.cache[path]['is_git']

        is_git = os.path.isdir(os.path.join(path, ".git"))
        if not is_git:
            paren = os.path.abspath(os.path.join(path, ".."))
            if paren != path:
                is_git = GitDirectoryCache.is_git(paren)

        GitDirectoryCache.cache[path] = {'is_git': is_git, 'timeout': now + 5}

        return is_git


class GitExHelper():
    def is_enabled(self):
        path = self.get_path();
        if path is None:
            return False

        return GitDirectoryCache.is_git(path)

    # Call gitex with the given parameters.
    #
    # Example:
    #   self.gitex("about")
    def gitex(self, *arguments):
        arguments = list(arguments)
        arguments.insert(0, "gitex")
        call(arguments, shell=True)


class GitExCommand(GitExHelper, sublime_plugin.WindowCommand):
    def get_path(self):
        window = self.window
        view = self.window.active_view();
        if view and view.file_name():
            return os.path.dirname(view.file_name())

        folders = window.folders();
        for folder in folders:
            return folder

    def run(self):
      path = self.get_path()

      if path is not None:
          os.chdir(path)

          self.execute(path)


class GitExTextCommand(GitExHelper, sublime_plugin.TextCommand):
    def get_path(self):
        view = self.view;
        if view and view.file_name():
            return view.file_name()

    def run(self, edit):
      path = self.get_path()

      if path is not None:
          self.execute(path)


class GitExAbout(GitExCommand):
    def execute(self, path):
        self.gitex("about")

    def is_enabled(self):
        return True


class GitExBlame(GitExTextCommand):
    def execute(self, path):
        self.gitex("blame", path)


class GitExBranch(GitExCommand):
    def execute(self, path):
        self.gitex("branch")


class GitExBrowse(GitExCommand):
    def execute(self, path):
        self.gitex("browse")


class GitExCommit(GitExCommand):
    def execute(self, path):
        self.gitex("commit")


class GitExCheckoutbranch(GitExCommand):
    def execute(self, path):
        self.gitex("checkoutbranch")


class GitExCheckoutrevision(GitExCommand):
    def execute(self, path):
        self.gitex("checkoutrevision")


class GitExDiffTool(GitExTextCommand):
    def execute(self, path):
        self.gitex("difftool", path)


class GitExFileHistory(GitExTextCommand):
    def execute(self, path):
        self.gitex("filehistory", path)


class GitExInit(GitExCommand):
    def execute(self, path):
        print(path);
        self.gitex("init", path)

    def is_enabled(self):
        path = self.get_path();
        if path is None:
            return False

        return not GitDirectoryCache.is_git(path)


class GitExPull(GitExCommand):
    def execute(self, path):
        self.gitex("pull")


class GitExPush(GitExCommand):
    def execute(self, path):
        self.gitex("push")


class GitExSettings(GitExCommand):
    def execute(self, path):
        self.gitex("settings")

    def is_enabled(self):
        return True


class GitExTag(GitExCommand):
    def execute(self, path):
        self.gitex("tag")
