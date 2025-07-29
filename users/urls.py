from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path
from users.views import AssignRole, ChangePassword, CreateGroup, CustomLoginView, CustomPasswordResetConfirmView, CustomPasswordResetView, EditProfileView, GroupList, ProfileView, activate_user, admin_dashboard, delete_group, sign_up, sign_out

urlpatterns = [
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_in/", CustomLoginView.as_view(), name="sign_in"),
    path("sign_out/", LogoutView.as_view(), name="log_out"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin/dashboard/", admin_dashboard, name='admin_dashboard'), 
    path("admin/<int:user_id>/assign_role/", AssignRole.as_view(), name='assign_role'),
    path("admin/create_group/", CreateGroup.as_view(), name='create_group'),
    path("admin/group_list/", GroupList.as_view(), name='group_list'),
    path("admin/<int:group_id>delete_group/", delete_group, name='delete_group'),
    path("profile/", ProfileView.as_view(), name='profile'),
    path("password_change/", ChangePassword.as_view(), name='password_change'),
    path("password_change/done/", PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path("password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path("password_reset/confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("edit_profile/", EditProfileView.as_view(), name='edit_profile')
]
