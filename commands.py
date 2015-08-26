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


class GitExFileCommand(GitExHelper, sublime_plugin.TextCommand):
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
        call(["gitex.cmd", "about"], shell=True)

    def is_enabled(self):
        return True


class GitExBlame(GitExFileCommand):
    def execute(self, path):
        call(["gitex.cmd", "blame", path], shell=True)


class GitExBranch(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "branch"], shell=True)


class GitExBrowse(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "browse"], shell=True)


class GitExCommit(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "commit"], shell=True)


class GitExCheckoutbranch(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "checkoutbranch"], shell=True)


class GitExCheckoutrevision(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "checkoutrevision"], shell=True)


class GitExDiffTool(GitExFileCommand):
    def execute(self, path):
        call(["gitex.cmd", "difftool", path], shell=True)


class GitExFileHistory(GitExFileCommand):
    def execute(self, path):
        call(["gitex.cmd", "filehistory", path], shell=True)


class GitExInit(GitExCommand):
    def execute(self, path):
        print(path);
        call(["gitex.cmd", "init", path], shell=True)

    def is_enabled(self):
        path = self.get_path();
        if path is None:
            return False

        return not GitDirectoryCache.is_git(path)


class GitExPull(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "pull"], shell=True)


class GitExPush(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "push"], shell=True)


class GitExSettings(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "settings"], shell=True)

    def is_enabled(self):
        return True


class GitExTag(GitExCommand):
    def execute(self, path):
        call(["gitex.cmd", "tag"], shell=True)
