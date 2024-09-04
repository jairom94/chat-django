from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/',views.Login,name='Login'),
    path('logout/',views.Logout,name='Logout'),
    path('register/',views.Register,name='Register'),
    path('dashboard/',views.Dashboard,name='Dashboard'),
    path('dashboard/type-user/',views.CreateTypeUser,name='CreateTypeUser'),
    path('profile/',views.ProfileView,name='Profile'),
    path('profile/edit/<user_id>',views.EditProfile,name='EditProfile')
    
]


