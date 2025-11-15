from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('product/', views.product, name='product'), 
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('category/<int:cat_id>/', views.category_list, name='category_list'),
    path('knowledge', views.knowledge, name='knowledge'),
    path('contact', views.contact, name='contact'),  
]
