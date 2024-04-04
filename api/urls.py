from django.urls import path
from .views import *

urlpatterns = [
    path('logout-all-devices', LogoutAllView.as_view(), name='auth_logout'),
    path('menu-items', MenuItemView.as_view()),
    path('menu-items/category', CategoryView.as_view()),
    path('menu-items/<int:pk>', SingleItemView.as_view()),
    path('groups/manager/users/', ManagerUsersView.as_view()),
    path('groups/manager/users/<int:pk>/', ManagerSingleUserView.as_view()),
    path('groups/delivery-crew/users/', Delivery_crew_management.as_view()),
    path('groups/delivery-crew/users/<int:pk>/', Delivery_crew_management_single_view.as_view()),
    path('cart/menu-items/', Customer_Cart.as_view()),
    path('orders/', OrdersView.as_view()),
    path('orders/<int:pk>', SingleOrderView.as_view()),
]