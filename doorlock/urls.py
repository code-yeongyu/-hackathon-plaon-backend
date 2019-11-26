"""plaon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import doorlock.views as views

urlpatterns = [
    path('invite/<int:beacon_id>', views.invite, name='invite'),
    path('open/<int:beacon_id>/', views.send_open_push, name='open'),
    path('<int:pk>/', views.DoorlockDetail.as_view(), name='doorlockDetail'),
    path('', views.DoorlockOverall.as_view(), name='doorlockOverall')
]
