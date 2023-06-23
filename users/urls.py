from django.urls import path
from users.views import HomeView,LoginView,SignupView,TokenVerificationView,LogOutView



urlpatterns = [
    path('',HomeView.as_view(),name='homepage'),
    path('login/',LoginView.as_view(),name='login_page'),
    path('signup/',SignupView.as_view(),name='signup_page'),
    path('logout/',LogOutView.as_view(),name='logout_page'),
    path('user/verification/<str:token>',TokenVerificationView.as_view(),name='email_verification_page'),
]