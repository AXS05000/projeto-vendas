from django.urls import path

from .views import FormularioDeVendaCreateView, index, login

urlpatterns = [
    path('', index, name='index'),
    path('formulariodevenda/', FormularioDeVendaCreateView.as_view(),
         name='formulariodevenda'),
    path('login/', login, name='login'),

]
