from django.urls import path
from .views import registration, loginview, logoutview, userprofile, edit_user_profile, edit_user, password_reset_request, change_password
from django.contrib.auth import views as auth_views #import this

app_name = 'user'


urlpatterns = [
    path('registration/', registration, name='signup'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
    
    path('profile/<int:id>', userprofile, name="profile"),
    path('edit_profile/', edit_user_profile, name="edit-profile"),
    path('edit_user/', edit_user, name="edit-user"),
    
    path('password_change/', change_password, name="password_change"),
   #path('password_change_done', auth_views.PasswordChangeDoneView.as_view(template_name="user/change_password_done.html"), name="password_change_done"),
    
    path("password_reset/", password_reset_request, name="password_reset"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="user/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password/password_reset_complete.html'), name='password_reset_complete'),      

]