import sys
sys.dont_write_bytecode = True
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WarmupProject.settings")
import django
django.setup()
