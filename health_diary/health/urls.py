from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('diary/', views.diary, name='diary'),
    path('diary/edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('diary/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
]
