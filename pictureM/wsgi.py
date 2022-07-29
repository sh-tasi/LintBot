"""
WSGI config for pictureM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append('/Users/oyste/lib/miniconda3')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pictureM.settings')

application = get_wsgi_application()
