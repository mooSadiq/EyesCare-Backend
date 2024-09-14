from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, PostListSerializer
from .filters import PostFilter

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 6  
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'total_items': self.page.paginator.count,
            'results': data
        })


class PostListView(APIView):
    pagination_class = CustomPagination
    filterset_class = PostFilter

    def get(self, request):
        posts = Post.objects.all()

        filterset = self.filterset_class(request.query_params, queryset=posts)
        if not filterset.is_valid():
            return Response({'message': 'معلمات الفلترة غير صحيحة تأكد منها!'}, status=400)
        
        filtered_posts = filterset.qs

        total_posts_count = posts.count()

        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(filtered_posts, request)
        serializer = PostListSerializer(paginated_posts, many=True, context={'request': request})

        return paginator.get_paginated_response({
            'posts': serializer.data,
            'total_posts_count': total_posts_count  
        })
        
def index(request):
  return render(request, 'posts_list.html')

def postDetails(request):
  return render(request, 'post_details.html')
