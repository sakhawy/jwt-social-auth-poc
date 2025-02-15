from django.urls import path
from .views import GoogleLoginView, GoogleCallbackView, ProtectedView

app_name = 'authapp'

urlpatterns = [
    path('login/google/', GoogleLoginView.as_view(), name='google-login'),
    path('login/google/callback/', GoogleCallbackView.as_view(), name='google-callback'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
