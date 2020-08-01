from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('user_center/<username>/', views.user_center, name='user_center'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_info/<user_id>/', views.edit_info, name='edit_info'),

]