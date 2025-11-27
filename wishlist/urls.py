from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_wishlist, name='my_wishlist'),
    path('mine/item/add/', views.ItemCreateView.as_view(), name='item_add'),
    path('mine/item/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('mine/item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('users/', views.select_user_view, name='select_user'),
    path('user/<str:username>/', views.user_wishlist_view, name='user_wishlist'),

    path('<str:username>/', views.public_wishlist, name='public_wishlist'),
    path('<str:username>/item/<int:pk>/purchase/', views.mark_purchased_view, name='item_purchase'),
]
