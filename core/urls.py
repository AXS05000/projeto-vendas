from django.urls import path

from .views import (DashListView, FormularioDeVendaCreateView, VendaListView,
                    billing, index, login, notifications, profile, rtl,
                    sign_in, sign_up, tables, virtual_reality)

urlpatterns = [
    path('', index, name='index'),
    path('formulariodevenda/', FormularioDeVendaCreateView.as_view(),
         name='formulariodevenda'),
    path('login/', login, name='login'),
    path('sale_list/', VendaListView.as_view(),
         name='sale_list'),
    path('dashboard/', DashListView.as_view(), name='dashboard'),
    path('tables/', tables, name='tables'),
    path('billing/', billing, name='billing'),
    path('virtual_reality/', virtual_reality, name='virtual_reality'),
    path('rtl/', rtl, name='rtl'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', profile, name='profile'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_up/', sign_up, name='sign_up'),


]
