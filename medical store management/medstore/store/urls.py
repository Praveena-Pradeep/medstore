# store/urls.py
from django.urls import path
from .views import signup
from .views import add_medicine, medicine_list
from .views import edit_medicine, delete_medicine
from .views import user_logout
from .views import signup
from . import views
from .views import CustomLoginView


urlpatterns = [
     path('', views.home, name='home'), 
  path('login/', views.login_page, name='login_page'),  # This is where the issue might lie

    path('signup/', signup, name='signup'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('medicine_list/', medicine_list, name='medicine_list'),

    path('edit_medicine/<int:medicine_id>/', edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),

    path('logout/', user_logout, name='logout'),
  
]
