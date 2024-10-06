from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .models import Review
from apps.users.models import CustomUser
from .serializer import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
def evaluations_page(request):
    return render(request, "app_reviews.html")


#عرض التقيمات
class ReviewsListView(APIView):
    def get(self,request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        if serializer.data:
            return Response({"Reviews":serializer.data},status.HTTP_200_OK)
        else:
            return Response({"Info":"There is not any reviews"},status.HTTP_404_NOT_FOUND)

#حذف تقيم
class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request, pk):
        review = get_object_or_404(Review,id=pk)
        serializer = ReviewSerializer(review, many=False)
        if not serializer.data:
            return Response({"message":"لم يتم إيجاد التقيم"},status.HTTP_404_NOT_FOUND)
        else:
            result=review.delete()
        if result:
            return Response({"message":"تم الحذف بنجاح!"},status.HTTP_200_OK)
        else:
            return Response({"message":" لم يتم الحذف "},status.HTTP_400_BAD_REQUEST)

