from notifications.models import Notification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import NotificationSerializer

@api_view(['GET'])
def get_notification(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    unread_count = Notification.objects.filter(unread=True).count()
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


@api_view(['POST'])
def read_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        # Check if the notification is already read
        if not notification.unread:
            return Response({
                'message': 'الاشعار بالفعل مقروء'
            }, status=status.HTTP_200_OK)
        notification.unread = False
        notification.save()
        return Response({
            'message': 'تم تحويل الاشعار إلى مقروء بنجاح'
        }, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({
            'message': 'لم يتم العثور على الاشعار'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def read_all_notifications(request):
    unread_notifications = Notification.objects.filter(unread=True)
    if unread_notifications.exists():
        unread_notifications.update(unread=False)
        return Response({
            'message': 'تم تحويل جميع الإشعارات إلى مقروءة بنجاح'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'message': 'لا توجد إشعارات غير مقروءة'
        }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return Response({
            'message': 'تم حذف الإشعار بنجاح'
        }, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({
            'message': 'لم يتم العثور على الإشعار'
        }, status=status.HTTP_404_NOT_FOUND)
