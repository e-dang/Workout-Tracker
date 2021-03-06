"""workout_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

API_VERSION = 'v1'
PREFIX_API_URL = f'api/{API_VERSION}/'

extra_patterns = [
    path('auth/', include('auth.urls')),
    path('users/', include('users.urls')),
    path('muscles/', include('muscles.urls')),
    path('equipment/', include('equipment.urls')),
    path('movements/', include('movements.urls')),
    path('exercises/', include('exercises.urls')),
    path('workouts/', include('workouts.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{PREFIX_API_URL}', include(extra_patterns))
]
