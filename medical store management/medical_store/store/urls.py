from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('add_stock/<int:medicine_id>/', views.add_stock, name='add_stock'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('search/', views.search_medicines, name='search_medicines'),
    path('edit_medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('logout/', views.logout_view, name='logout'),
]
