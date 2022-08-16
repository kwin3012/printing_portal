from django.urls import path
from users import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('place_order/',views.Place_Order,name='place_order'),
    path('order_pending/',views.Order_Pending,name='order_pending'),
    path('order_history/',views.Order_History,name='order_history'),
    path('recent_orders/',views.Recent_Orders,name='recent_orders'),
    path('status_change/<int:order_id>',views.Status_Change,name="status_change"),
    path('printed_orders/',views.Printed_Orders,name='printed_orders'),
    path('check_otp/<int:order_id>',views.Check_OTP,name='check_otp'),
    path('completed_orders/',views.Completed_Orders,name='completed_orders'),
    path('download/<int:order_id>',views.Download,name='download'),
    path('pay/',views.Gateway1, name = 'gateway1'),
    path('pay/<int:order_id>',views.Gateway2, name = 'gateway2'),
    path('pay/success/',views.success, name = 'success'),
]
