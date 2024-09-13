#!/usr/bin/env python
"""Command-line utility for executing administrative tasks."""

import os
import sys
from warnings import warn

from django.core.management import execute_from_command_line


def main() -> None:  # pragma: nocover
    """Parse the commandline and run administrative tasks."""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keystone_api.main.settings')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':  # pragma: nocover
    warn("You are calling `manage.py' directly. Use the bundled `keystone-api` command instead.", RuntimeWarning)
    main()
