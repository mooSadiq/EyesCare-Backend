from rest_framework.decorators import api_view
from .models import Review
from apps.users.models import CustomUser
from .serializer import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

#عرض التقيمات
class ReviewsListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True,context={'request': request})
        if serializer.data:
            return Response({"status":True,"code":200,"message":"لقد تم جلب البيانات بنجاح","data":serializer.data},status.HTTP_200_OK)
        else:
            return Response({"status":False,"code":404,"Info":"لا يوجد أي بيانات"},status.HTTP_404_NOT_FOUND)

class SetReviewsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user_id = request.data.get('user')
        if not user_id:
            return Response({"status": False,"code": 400,"message": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"status": False,"code": 404,"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        user_reviews = Review.objects.filter(user=user)
        if user_reviews.exists():
            return Response({"status": False,"code": 302,"message": "لديك تقييم بالفعل، إذا أردت يمكنك تعديله."}, status=status.HTTP_302_FOUND)
        else:
            Review.objects.create(
                user=user,
                rating=request.data['rating'],
                comment=request.data['comment']
            )
            return Response({"status": True,"code": 201,"message": "تم إضافة التقييم بنجاح"}, status=status.HTTP_201_CREATED)



#حذف تقيم
class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request, pk):
        review = get_object_or_404(Review,id=pk)
        serializer = ReviewSerializer(review, many=False)
        if not serializer.data:
            return Response({"code":404,"status":False,"message":"لم يتم إيجاد التقيم"},status.HTTP_404_NOT_FOUND)
        else:
            result=review.delete()
        if result:
            return Response({"code":200,"status":True,"message":"تم الحذف بنجاح!"},status.HTTP_200_OK)
        else:
            return Response({"code":400,"status":False,"message":" لم يتم الحذف "},status.HTTP_400_BAD_REQUEST)

#تعديل تقييم
class UpdateReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request, pk):
        try:
            review = Review.objects.get(id=pk)
        except Review.DoesNotExist:
            return Response({"code":404,"status":False,'message': 'لم يتم إيجاد التقييم المطلوب'}, status=status.HTTP_404_NOT_FOUND)
        new_comment = request.data.get('comment', review.comment)  # تعديل التعليق إذا تم توفيره
        new_rating = request.data.get('rating', None)  # جلب التقييم الجديد إذا تم توفيره
        if new_rating is not None:
            # حساب المتوسط بين التقييم القديم والجديد
            average_rating = (review.rating + int(new_rating)) / 2
            review.rating = average_rating  # تحديث التقييم إلى المتوسط
        review.comment = new_comment
        review.save()
        serializer = ReviewSerializer(review)
        if serializer.data:
            return Response({"code":200,"status":True,"message":"لقد تم التعديل بنجاح"}, status=status.HTTP_200_OK)
        else:
            return Response({"code":400,"status":False,"message":"لم يتم التعديل !"}, status=status.HTTP_400_BAD_REQUEST)