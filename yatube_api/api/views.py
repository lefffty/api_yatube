from django.http import HttpRequest
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    ViewSet,
    GenericViewSet,
)
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.mixins import (
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework import status

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


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = PostSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetPutPatchDeleteViewSet(
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    pass


class PostViewSet(GetPutPatchDeleteViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(
            post_id=post_id,
        )
        return post

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        post = self.get_queryset()
        if post.author != request.user and request.user.is_authenticated:
            return Response(
                data=request.data,
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(
            post,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_PARTIAL_CONTENT
            )
        return Response(status=status.HTTP_403_BAD_REQUEST)

    def update(self, request: HttpRequest, *args, **kwargs):
        post = self.get_queryset()
        if post.author != request.user and request.user.is_authenticated:
            return Response(
                data=request.data,
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_202_ACCEPTED
            )

    def destroy(self, request: HttpRequest, *args, **kwargs):
        post = self.get_queryset()
        if post.author != request.user and request.user.is_authenticated:
            return Response(
                data=request.data,
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_202_ACCEPTED
            )


class GroupListCreateViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        new_queryset = Comment.objects.filter(post_id=post_id)
        return new_queryset


class CommentViewSet(ViewSet):
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        comments = Comment.objects.filter(
            post_id=post_id
        )
        comment_id = self.kwargs.get('comment_id')
        comment = comments.get(
            comment_id=comment_id
        )
        return comment

    def retrieve(self, request: HttpRequest):
        comment = self.get_queryset()
        serializer = CommentSerializer(
            comment
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def update(self, request: HttpRequest):
        comment = self.get_queryset()
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request: HttpRequest):
        comment = self.get_queryset()
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: HttpRequest):
        comment = self.get_queryset()
        comment.delete()
        return Response(
            status=status.HTTP_200_OK
        )
