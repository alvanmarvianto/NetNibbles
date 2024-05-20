from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('promo/', views.promo, name="promo"),
    path('store/', views.store, name="store"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('success/', views.success, name="success"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('logout/', views.logout, name='logout'),
]
