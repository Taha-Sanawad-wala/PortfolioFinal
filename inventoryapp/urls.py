from django.contrib import admin
from django.urls import path
from inventoryapp.views import index,login,signup,logout,update,delete,addProduct,dashboard
urlpatterns = [
    path('',index,name='home_inventory'),
    path('login/',login),
    path('signup/',signup),
    path('logout/',logout),
    path('update/<id>',update),
    path('delete/<id>',delete),
    path('addproduct/',addProduct),
    path('dashboard/',dashboard)
]