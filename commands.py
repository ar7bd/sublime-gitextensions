import sublime_plugin
import sublime

import os
from subprocess import call

class GitExCommand(sublime_plugin.WindowCommand):
    def get_path(self):
        window = self.window
        view = self.window.active_view();
        if view and view.file_name():
            return os.path.dirname(view.file_name())

        folders = window.folders();
        for folder in folders:
            return folder

    def is_enabled(self):
        return self.get_path() is not None

    def run(self):
      path = self.get_path()

      if path is not None:
          os.chdir(path)

          self.call(path)


class GitExFileCommand(sublime_plugin.TextCommand):
    def get_path(self):
        view = self.view;
        if view and view.file_name():
            return view.file_name()

    def is_enabled(self):
        return self.get_path() is not None

    def run(self, edit):
      path = self.get_path()

      if path is not None:
          self.call(path)


class GitExAbout(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "about"], shell=True)


class GitExBlame(GitExFileCommand):
    def call(self, path):
      call(["gitex.cmd", "blame", path], shell=True)


class GitExBranch(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "branch"], shell=True)


class GitExBrowse(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "browse"], shell=True)


class GitExCommit(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "commit"], shell=True)


class GitExCheckoutbranch(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "checkoutbranch"], shell=True)


class GitExCheckoutrevision(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "checkoutrevision"], shell=True)


class GitExDiffTool(GitExFileCommand):
    def call(self, path):
      call(["gitex.cmd", "difftool", path], shell=True)


class GitExFileHistory(GitExFileCommand):
    def call(self, path):
      call(["gitex.cmd", "filehistory", path], shell=True)


class GitExInit(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "init", path], shell=True)


class GitExPull(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "pull"], shell=True)


class GitExPush(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "push"], shell=True)


class GitExSettings(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "settings"], shell=True)


class GitExTag(GitExCommand):
    def call(self, path):
      call(["gitex.cmd", "tag"], shell=True)
