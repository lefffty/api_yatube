from django.http import HttpRequest
from django.shortcuts import get_object_or_404
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
            serializer.validated_data['author'] = request.user
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
            status=status.HTTP_204_NO_CONTENT,
        )
