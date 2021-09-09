from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('safe_shopping/', views.safe_shopping, name='storedetails'),
    path('delivery/', views.delivery, name='delivery'),
    path('returns/', views.returns, name='returns'),
]
