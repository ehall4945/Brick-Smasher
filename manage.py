import os
import sys


# Runs Django management commands for this project
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BrickSmasher.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Could not import Django") from exc

    execute_from_command_line(sys.argv)
