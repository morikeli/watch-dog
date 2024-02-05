from django.urls import path
from . import views
from . import validators


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout_user'),   
]

htmx_urlpatterns = [
    path('validate-username/', validators.check_username_exists, name='validate_username'),
    path('validate-email/', validators.email_address_validation, name='validate_email'),
    path('validate-mobile/', validators.mobile_number_validation, name='validate_mobile_number'),
    path('validate-age/', validators.date_and_users_age_validation, name='validate_age'),
    path('check-password/', validators.password_match_and_length_validation, name='check_password'),
]

urlpatterns += htmx_urlpatterns