from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.home, name="home"),
    path('index/',views.index, name="index"),
    path('main/',views.main, name="main"),
    path('admin-login/',views.adminLogin, name="admin_login"),
    path('adminhome/',views.adminHome, name="adminhome"),
    path('admindashboard/',views.admin_dashboard, name="admindashboard"),
    path('add-category/',views. add_category, name="add_category"),
    path('view-category/',views. view_category, name="view-category"),
    path('edit-category/<int:pid>/', views.edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', views.delete_category, name="delete_category"),
    path('create_team/', views.create_team, name='create_team'),
    path('registration/', views.registration, name="registration"),
    path('userlogin/',views.userlogin, name="userlogin"),
    path('profile/',views. profile, name="profile"),
    path('logout/', views.logoutuser, name="logout"),
    path('adminlogout/', views.adminlogout, name="adminlogout"),
    path('change-password/', views.change_password, name="change_password"),
    path('join_team/<int:pid>/', views.view_team, name="join_team"),
    path('team_detail/<int:pid>/', views.team_detail, name="team_detail"),
    #path('view_opponents/', views.view_opponents, name='view_opponents'),
    #notification
    #path('notifications/', views.view_notifications, name='view_notifications'),
    path('search_opponents/', views.search_opponents, name='search_opponents'),
    path('challenge_opponent/<str:team_captain_username>/', views.challenge_opponent, name='challenge_opponent'),
     #path('notifications/', views.notification_panel, name='notification_panel'),
     #path('fetch_nearby_teams/', views.fetch_nearby_teams, name='fetch_nearby_teams'),
    #notificationurls
    path('accept_challenge/<int:challenge_id>/', views.accept_challenge, name='accept_challenge'),
    path('reject_challenge/<int:challenge_id>/', views.reject_challenge, name='reject_challenge'),
    
    path('chat/<str:opponent_username>/', views.chat_view, name='chat_view'),
   
]# urls.py

# gullyapp/urls.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
