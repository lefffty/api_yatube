from django.http import HttpRequest
from django.shortcuts import get_object_or_404
# from rest_framework.viewsets import (
#     ModelViewSet,
#     ReadOnlyModelViewSet,
#     GenericViewSet,
# )
# from rest_framework.generics import (
#     ListCreateAPIView,
# )
# from rest_framework.mixins import (
#     RetrieveModelMixin,
#     DestroyModelMixin,
#     UpdateModelMixin,
# )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
)

from posts.models import (
    Post,
    Comment,
    Group,
)
from posts.serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer
)


@api_view(['GET', 'POST'])
def api_posts(request: HttpRequest) -> Response:
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts,
            many=True,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST':
        serializer = PostSerializer(
            data=request.data,
        )
        if serializer.is_valid() and request.user.is_authenticated:
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def api_post_detail(request: HttpRequest, post_id) -> Response:
    post = get_object_or_404(
        Post,
        pk=post_id,
    )
    if request.method == 'GET':
        serializer = PostSerializer(
            post,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PATCH' or request.method == 'PUT':
        if request.user != post.author:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        post.delete()
        return Response(
            data=post,
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(['GET'])
def api_groups(request: HttpRequest) -> Response:
    groups = Group.objects.all()
    serializer = GroupSerializer(
        groups,
        many=True,
    )
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
def api_group_detail(request: HttpRequest, group_id) -> Response:
    group = get_object_or_404(
        Group,
        pk=group_id,
    )
    serializer = GroupSerializer(
        group,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
def api_comments(request: HttpRequest, post_id) -> Response:
    post = get_object_or_404(
        Post,
        pk=post_id,
    )
    if request.method == 'GET':
        comments = Comment.objects.filter(
            post_id__exact=post_id,
        )
        serializer = CommentSerializer(
            comments,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST' and request.user.is_authenticated:
        serializer = CommentSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.validated_data['post'] = post
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def api_comment_detail(request: HttpRequest, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
    )
    if request.method == 'GET':
        serializer = CommentSerializer(
            comment,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'PUT' or request.method == 'PATCH':
        if request.user != comment.author:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        comment.delete()
        return Response(
            comment,
            status=status.HTTP_204_NO_CONTENT,
        )
# class PostsViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def create(self, request: HttpRequest, *args, **kwargs):
#         serializer = PostSerializer(
#             data=request.data,
#         )
#         if serializer.is_valid():
#             serializer.instance.author = request.user
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             serializer.data,
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class GetPutPatchDeleteViewSet(
#     RetrieveModelMixin,
#     DestroyModelMixin,
#     UpdateModelMixin,
#     GenericViewSet
# ):
#     pass


# class PostViewSet(GetPutPatchDeleteViewSet):
#     serializer_class = PostSerializer

#     def perform_update(self, serializer):
#         if serializer.instance.author != self.request.user:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN
#             )

#     def perform_destroy(self, instance):
#         if instance.author != self.request.user:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     def get_object(self):
#         post_id = self.kwargs.get('post_id')
#         post = Post.objects.get(
#             pk=post_id,
#         )
#         return post

#     def partial_update(self, request: HttpRequest, *args, **kwargs):
#         post = self.get_queryset()
#         serializer = self.serializer_class(
#             post,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_PARTIAL_CONTENT
#             )
#         return Response(status=status.HTTP_403_BAD_REQUEST)

#     def update(self, request: HttpRequest, *args, **kwargs):
#         post = self.get_queryset()
#         serializer = self.serializer_class(
#             post,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_202_ACCEPTED
#             )

#     def destroy(self, request: HttpRequest, *args, **kwargs):
#         post = self.get_queryset()
#         serializer = self.serializer_class(
#             post,
#             data=request.data,
#             partial=True,
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_202_ACCEPTED
#             )


# class GroupListCreateViewSet(ReadOnlyModelViewSet):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


# class CommentsViewSet(ListCreateAPIView):
#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         post_id = self.kwargs.get('post_id')
#         new_queryset = Comment.objects.filter(post_id=post_id)
#         return new_queryset


# class CommentViewSet(GetPutPatchDeleteViewSet):
#     def get_object(self):
#         post_id = self.kwargs.get('post_id')
#         comment_id = self.kwargs.get('comment_id')
#         comment = Comment.objects.filter(
#             pk=comment_id,
#             post_id=post_id,
#         )
#         return comment

#     def perform_update(self, serializer):
#         if self.request.user != serializer.instance.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     def perform_destroy(self, instance):
#         if self.request.user != instance.author:
#             return Response(
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#     def retrieve(self, request: HttpRequest):
#         comment = self.get_object()
#         serializer = CommentSerializer(
#             comment
#         )
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def update(self, request: HttpRequest):
#         comment = self.get_queryset()
#         serializer = CommentSerializer(
#             comment,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_202_ACCEPTED
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def partial_update(self, request: HttpRequest):
#         comment = self.get_queryset()
#         serializer = CommentSerializer(
#             comment,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_202_ACCEPTED
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request: HttpRequest):
#         comment = self.get_queryset()
#         comment.delete()
#         return Response(
#             status=status.HTTP_200_OK
#         )
