from notifications.models import Notification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import NotificationSerializer

@api_view(['GET'])
def get_notification(request):
    notifications = Notification.objects.filter(unread=True)
    serializer = NotificationSerializer(notifications, many=True)
    unread_count = notifications.count()
    if serializer.data:
        return Response({
                        'message': 'تم العثور على نتيجة',
                        'data': serializer.data,
                        'count':unread_count
        },status=status.HTTP_200_OK)
    else:
        return Response({
                        'message': 'لم يتم العثور على نتيجة',
        },status=status.HTTP_404_NOT_FOUND)
