from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('store/', views.menu, name="store"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('success/', views.success, name="success"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_page, name='user_page'),
    path('orderhistory/', views.orderHistory, name='orderhistory'),
    path('menu/', views.menu, name="menu"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('tnc/', views.tnc, name="tnc"),
    path('hns/', views.hns, name="hns"),
]
