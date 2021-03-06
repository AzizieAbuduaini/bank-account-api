"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
from core.config.local import *
DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['thunes.globalpeacelove.com', 'http://thunes.globalpeacelove.com']
