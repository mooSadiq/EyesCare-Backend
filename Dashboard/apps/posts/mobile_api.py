import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Post, PostImage, Like
from .serializers import PostListSerializer, PostSerializer

class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        accept_language = request.headers.get('Accept-Language', None)
        print("Accept-Language:", accept_language)
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'وريحهم',
            'data': serializer.data
        })


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المنشور غير موجود',
            })

        serializer = PostListSerializer(post, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم جلب المنشور بنجاح',
            'data': serializer.data,
        })

class UserPostsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # تصفية المنشورات الخاصة بالمستخدم الحالي
        posts = Post.objects.filter(user=request.user).prefetch_related('user')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم جلب المنشورات بنجاح',
            'data': serializer.data
        })

              
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)        
        if serializer.is_valid():
            post = serializer.save(user=request.user)        
            image = request.FILES.get('image')            
            if image:
                PostImage.objects.create(post=post, image=image)            
            return Response({
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': 'تم ارسال المنشور بنجاح',
            })
        
        return Response({
            'status': False,
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'فشل',
        })


class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk).first()
        if not post:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المنشور غير موجود',
            })
        if hasattr(post, 'image') and post.image:
            image_path = post.image.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)            
            post.image.delete()
                            
        post.delete()
        return Response({
            'status': True,
            'code': status.HTTP_204_NO_CONTENT,
            'message': 'تم حذف المنشور بنجاح',
        })
        

class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        post = Post.objects.filter(id=pk, user=request.user).first()
        if not post:
            return Response({
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'المنشور غير موجود',
            })

        new_text = request.data.get('text')
        if new_text is not None:
            post.text = new_text

        new_img = request.FILES.get('image')
        delete_img = request.data.get('delete_image', False)

        if delete_img:
            if hasattr(post, 'image') and post.image:
                old_image_path = post.image.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
                post.image.delete()
                post.image = None

        if new_img:
            if hasattr(post, 'image') and post.image:
                old_image_path = post.image.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
                post.image.delete()
            PostImage.objects.create(post=post, image=new_img)

        post.save()

        return Response({
            'status': True,
            'code': status.HTTP_200_OK,
            'message': 'تم تعديل المنشور بنجاح',
        })
            
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        user = request.user

        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            existing_like.delete()
            post.likes_count = post.likes.count()
            post.save()
            return Response({
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'ازالة الاعجاب',
            })
        else:
            Like.objects.create(user=user, post=post)
            post.likes_count = post.likes.count()
            post.save()
            return Response({
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': 'اعجاب',
            })

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostListSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
