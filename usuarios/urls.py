from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usuario/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
]
