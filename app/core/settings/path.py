import sys
from os.path import abspath, basename, dirname, join, normpath

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

STATICFILES_DIRS = []

STATIC_ROOT = join(PROJECT_ROOT, "static")

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, "templates"),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, "apps")))

# the URL for static files
STATIC_URL = "/static/"

# the URL for media files
MEDIA_URL = "/media/"
