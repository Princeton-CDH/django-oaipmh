"""
Test URL configuration for django_oaipmh
"""

from django.urls import path
from .views import OAIProvider

urlpatterns = [
    path('oai/', OAIProvider.as_view(), name='oai')
]
