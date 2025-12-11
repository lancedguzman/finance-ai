from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('tracker/', views.tracker, name='tracker'),
    path('api/categories/', views.category_list, name='category_list'),
    path('api/transactions/', views.transaction_list, name='transaction_list'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('edit-transaction/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('add-category/', views.add_category, name='add_category'),
]