#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SiteZ.settings.dev")
>>>>>>> f2079d21f8d69e5e8c102949a7b7ea2cda6ff006

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
