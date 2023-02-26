from django.urls import path

from .views import (DashListView, FormularioDeVendaCreateView, VendaListView,
                    extrato, notifications, profile, sign_in, tables)

urlpatterns = [
    path('formulariodevenda/', FormularioDeVendaCreateView.as_view(),
         name='formulariodevenda'),
    path('sale_list/', VendaListView.as_view(),
         name='sale_list'),
    path('dashboard/', DashListView.as_view(), name='dashboard'),
    path('tables/', tables, name='tables'),
    path('extrato/', extrato, name='extrato'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', profile, name='profile'),
    path('sign_in/', sign_in, name='sign_in'),



]
