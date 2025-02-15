from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class GoogleLoginView(APIView):
    def get(self, request):
        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name='google-oauth2',
            redirect_uri=settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL
        )

        auth_url = backend.auth_url()
        return redirect(auth_url)

class GoogleCallbackView(APIView):
    def get(self, request):
        strategy = load_strategy(request)
        backend = load_backend(
            strategy=strategy,
            name='google-oauth2',
            redirect_uri=settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL
        )

        try:
            user = backend.complete(request=request)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'You are authenticated!',
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
