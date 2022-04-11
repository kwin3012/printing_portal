from django.urls import path
from users import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('place_order/',views.Place_Order,name='place_order'),
    path('order_history/',views.Order_History,name='order_history'),
    path('recent_orders/',views.Recent_Orders,name='recent_orders'),
    path('status_change/<int:order_id>',views.Status_Change,name="status_change"),
]
