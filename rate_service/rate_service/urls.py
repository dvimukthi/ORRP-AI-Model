"""
URL configuration for rate_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from api.views import event_list, event_create, get_best_room_rates

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/events/", event_list, name='event-list'),
    path('api/events/create/', event_create, name='api-event-create'),
    path('api/events/get_best_room_rates/', get_best_room_rates, name='api-event-getbestrates'),
    
]
