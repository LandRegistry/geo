#!/bin/bash
export PYTHONPATH=/vagrant/apps/geo:${PYTHONPATH}
export DJANGO_SETTINGS_MODULE=geo.settings

django-admin.py runserver $PORT