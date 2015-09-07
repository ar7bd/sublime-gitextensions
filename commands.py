import sublime_plugin
import sublime

import os
import time
from subprocess import call

class GitDirectoryCache(object):
    '''
    Cached lookup for whether a directory is a git repository or not.
    '''
    cache = {}

    @classmethod
    def is_git(cls, path):
        '''
        Checks whether a given directory is part of a git repository.
        Returns True or False.
        '''
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
        path = self.get_path()
        if path is None:
            return False

        return GitDirectoryCache.is_git(path)

    @classmethod
    def gitex(cls, *arguments):
        '''
        Call gitex with the given parameters.

        Example:
          GitExHelper.gitex("about")
        '''
        gitex_command = GitExHelper.gitex_command()
        if gitex_command is None:
            print("Error: Could not find gitex command. ")
            return
        arguments = list(arguments)
        arguments = gitex_command + arguments
        call(arguments, shell=True)

    @classmethod
    def gitex_command(cls):
        '''
        Returns the GitExt command as array or None.
        '''
        settings = sublime.load_settings("GitExtensions.sublime-settings")
        gitex_command = []
        gitex_command_settings = settings.get("gitex_command", {})
        if sublime.platform() in gitex_command_settings:
            gitex_command = gitex_command_settings[sublime.platform()]
        if len(gitex_command) == 0:
            return None
        return gitex_command

    def execute(self, path):
        '''
        Will be executed with the file path of the file.
        Must be overriden by inherited classes.
        '''
        pass

    def get_path(self):
        '''
        Return path to the active file/ folder.
        '''
        pass


class GitExWindowCommand(GitExHelper, sublime_plugin.WindowCommand):
    def get_path(self):
        window = self.window
        view = self.window.active_view()
        if view and view.file_name():
            return os.path.dirname(view.file_name())

        folders = window.folders()
        for folder in folders:
            return folder

    def run(self):
        path = self.get_path()

        if path is not None:
            os.chdir(path)

            self.execute(path)


class GitExTextCommand(GitExHelper, sublime_plugin.TextCommand):
    def get_path(self):
        view = self.view
        if view and view.file_name():
            return view.file_name()

    def run(self, edit):
      path = self.get_path()

      if path is not None:
          self.execute(path)


class GitExAbout(sublime_plugin.WindowCommand):
    '''
    Calls GitExt about to open the about dialog.
    '''
    def run(self):
        GitExHelper.gitex("about")


class GitExBlame(GitExTextCommand):
    def execute(self, path):
        GitExHelper.gitex("blame", path)


class GitExBranch(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("branch")


class GitExBrowse(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("browse")


class GitExCommit(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("commit")


class GitExCheckoutbranch(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("checkoutbranch")


class GitExCheckoutrevision(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("checkoutrevision")


class GitExDiffTool(GitExTextCommand):
    def execute(self, path):
        GitExHelper.gitex("difftool", path)


class GitExFileHistory(GitExTextCommand):
    def execute(self, path):
        GitExHelper.gitex("filehistory", path)


class GitExInit(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("init", path)

    def is_enabled(self):
        path = self.get_path()
        if path is None:
            return False

        return not GitDirectoryCache.is_git(path)


class GitExPull(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("pull")


class GitExPush(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("push")


class GitExSettings(sublime_plugin.WindowCommand):
    def run(self):
        GitExHelper.gitex("settings")


class GitExTag(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("tag")


class GitExRemotes(GitExWindowCommand):
    def execute(self, path):
        GitExHelper.gitex("remotes")
