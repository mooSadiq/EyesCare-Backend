from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from .models import Review
from apps.users.models import CustomUser
from .serializer import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
def evaluations_page(request):
    return render(request, "app_reviews.html")


#عرض التقيمات
@api_view(['GET'])
def get_all_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    if serializer.data:
        return Response({"Reviews":serializer.data},status.HTTP_200_OK)
    else:
        return Response({"Info":"There is not any reviews"},status.HTTP_404_NOT_FOUND)

#عرض تقيم واحد
@api_view(['GET'])
def get_reviews_by_id(request,pk):
    reviews = get_object_or_404(Review,id=pk)
    serializer = ReviewSerializer(reviews, many=False)
    if serializer.data:
        return Response({"Review":serializer.data},status.HTTP_200_OK)
    else:
        return Response({"Info":"There is not any reviews"},status.HTTP_404_NOT_FOUND)



#حذف تقيم
@api_view(['DELETE'])
def delete_review(request, pk):
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

