import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from apps.users.models import CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
      try:
          first_name = request.data.get('name')
          email = request.data.get('email')
          profile_picture = request.data.get('image_url')
          provider='google'

          print(profile_picture)
          if not email:
                return Response({'error': 'Email not available'}, status=status.HTTP_400_BAD_REQUEST)
          user, created = CustomUser.objects.get_or_create(
              email=email,
              defaults={
                  'email': email,
                  'first_name': first_name,
                  'profile_picture': profile_picture,
                  'password': CustomUser.objects.make_random_password(),
                  'auth_provider':provider,
                  'user_type':'user',
                  'is_verified':True
              }
          )
          if not created:
                user.first_name = first_name
                user.auth_provider = provider
                user.profile_picture = profile_picture
                user.is_verified = True
                user.save()

          refresh = RefreshToken.for_user(user)              
          user_data = {
              'id': user.id,
              'email': user.email,
              'first_name': user.first_name,
              'user_type': user.user_type,
              'refresh': str(refresh),
              'access_token': str(refresh.access_token),
          }

          return Response({
              'status': True,
              'code': status.HTTP_200_OK,
              'message': 'تم إنشاء الحساب بنجاح',
              'data': user_data,
          }, status=status.HTTP_200_OK)
          
      except Exception as e:
          return Response({
              'status': False,
              'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
              "message": f"حدث خطأ أثناء  إنشاء الحساب: {str(e)}"
          }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          