from django.urls import path

from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, UserUpdateView, activate_new_user, \
    UsersListView, block_user

app_name = UsersConfig.name


urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('activate/<int:pk>/', activate_new_user, name='activate'),
    path('users_list/', UsersListView.as_view(), name='users_list'),
    path('block_user/<int:pk>', block_user, name='block_user')
]