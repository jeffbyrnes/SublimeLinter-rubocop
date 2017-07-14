#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jeff Byrnes
# Based on SublimeLinter-rubocop, written by Aparajita Fishman
# Contributors: Francis Gulotta, Josh Hagins, Mark Haylock
# Copyright (c) 2015-2016 The SublimeLinter Community
# Copyright (c) 2013-2014 Aparajita Fishman
# Copyright (c) 2017 Jeff Byrnes
#
# License: MIT
#

"""This module exports the Cookstyle plugin class."""

import os
from SublimeLinter.lint import RubyLinter, util


class Cookstyle(RubyLinter):
    """Provides an interface to cookstyle."""

    syntax = (
        'better rspec',
        'betterruby',
        'cucumber steps',
        'rspec',
        'ruby experimental',
        'ruby on rails',
        'ruby'
    )
    cmd = None
    executable = 'cookstyle'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.0.1'
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(:?(?P<warning>[RCW])|(?P<error>[EF])): '
        r'(?P<message>.+)'
    )
    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = r'\s*#'

    def cmd(self):
        """Build command, using STDIN if a file path can be determined."""

        command = ['cookstyle', '--format', 'emacs']

        # Set tempfile_suffix so by default a tempfile is passed onto rubocop:
        self.tempfile_suffix = 'rb'

        path = self.filename
        if not path:
            # File is unsaved, and by default unsaved files use the default
            # rubocop config because they do not technically belong to a folder
            # that might contain a custom .rubocop.yml. This means the lint
            # results may not match the rules for the currently open project.
            #
            # If the current window has open folders then we can use the
            # first open folder as a best-guess for the current projects
            # root folder - we can then pretend that this unsaved file is
            # inside this root folder, and rubocop will pick up on any
            # config file if it does exist:
            folders = self.view.window().folders()
            if folders:
                path = os.path.join(folders[0], 'untitled.rb')

        if path:
            # With this path we can instead pass the file contents in via STDIN
            # and then tell rubocop to use this path (to search for config
            # files and to use for matching against configured paths - i.e. for
            # inheritance, inclusions and exclusions).
            #
            # The 'force-exclusion' overrides rubocop's behavior of ignoring
            # global excludes when the file path is explicitly provided:
            command += ['--force-exclusion', '--stdin', path]
            # Ensure the files contents are passed in via STDIN:
            self.tempfile_suffix = None

        return command
