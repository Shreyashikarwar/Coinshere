from django.urls import path,include

from .views import *

urlpatterns = [
    path('signup/',signup),
    path('login/',login),
    path('logout/',user_logout),

    path('role-lists/',role_lists),
    # path('logout/', LogoutView.as_view(), name='auth_logout')

# UserProfile Data
    path('user-profile-list/<int:pk>/',user_profile_list),


# UserProfile Data Update
    path('user-profile-update/<int:pk>/',user_profile_update),

    path('update-avatar-image/',update_avatar_image),

    path('show-msg-already-login/',show_msg_user_already_login),

    path('user-login-check/',user_login_check),

    path('send-otp/',send_otp),

    path('reset-password/',reset_password),


]


