import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from apps.users.models import CustomUser
from rest_framework.views import APIView


class GoogleLoginView(APIView):
    def post(self, request):
        id_token_str = request.data.get('id_token')

        if not id_token_str:
            return Response({'error': 'No id_token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # تحقق من الرمز المميز مع جوجل
            id_info = id_token_str.verify_oauth2_token(
                id_token_str,
                request.Request(),
                'YOUR_CLIENT_ID.apps.googleusercontent.com'
            )

            # استخراج المعلومات من id_info
            email = id_info.get('email')
            first_name = id_info.get('given_name')
            last_name = id_info.get('family_name')
            google_id = id_info.get('sub')
            picture = id_info.get('picture')
            provider='google'

            if not email:
                return Response({'error': 'Email not available'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'profile_picture': picture,
                    'password': CustomUser.objects.make_random_password(),
                    'auth_provider':provider,
                    'is_verified':True
                }
            )

            # تحديث معلومات المستخدم إذا لزم الأمر
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.auth_provider = provider
                user.profile_picture = picture
                user.is_verified = True
                user.save()

            # توليد رموز JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_picture': user.profile_picture,
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
          
          