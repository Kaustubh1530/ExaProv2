from django.urls import path
from authentication import views
from django.conf.urls import url

urlpatterns = [

    path('admin-login/', views.admin_login, name="admin-login"),
    path('admin-home/', views.admin_home,name="admin-home"),
    path('admin-logout/', views.admin_logout,name="admin-logout"),
    path('user-signup/', views.user_signup, name="user-signup"),
    path('user-login/', views.user_login, name="user-login"),
    path('user-home/',views.user_home, name="user-home"),
    path('user-logout/', views.user_logout,name="user-logout"),
    path('verify/',views.verify, name="verify"),
    path('generate/',views.generate,name="generate"),
    path('change_pass/',views.change_pass, name="change_pass")
    
]
    