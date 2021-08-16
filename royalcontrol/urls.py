"""sistema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from royalcontrol import views
from django.urls                    import path



urlpatterns = [
    path('', views.cadAtendimento, name="cadAtendimento"),
    path('createEmpresa', views.createEmpresa, name="createEmpresa"),
    path('motivoChamado', views.motivoChamado, name="motivoChamado"),
    path(r'^redUpdate/(?P<id>\d+)$', views.redUpdate, name="redUpdate"),
    path('updateAtendimento', views.updateAtendimento, name="updateAtendimento"),
    path("graficosRegistro", views.graficosRegistro, name="graficosRegistro"),
    path(r'^redUpdateEmpresa/(?P<id>\d+)$', views.redUpdateEmpresa, name="redUpdateEmpresa"),
    
    
    path('filtrarRelatorio', views.filtrarRelatorio, name="filtrarRelatorio")
] 
