from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status



from posts.models import (Post,
                          Comment,
                          Group)
from posts.serializers import (PostSerializer,
                               CommentSerializer,
                               GroupSerializer)


ERR_403 = status.HTTP_403_FORBIDDEN
OK_200 = status.HTTP_200_OK
CREATED_201 = status.HTTP_201_CREATED
NO_CONTENT_204 = status.HTTP_204_NO_CONTENT


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GroupListCreateView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.Viewset):
    def retrieve(self, request, post_id):
        comments = Comment.objects.filter(
            post_id__exact=post_id,
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=OK_200)

    def create(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post_id=post_id)
            return Response(
                serializer.data,
                status=ERR_403,
            )


class CommentViewSet(viewsets.Viewset):
    def retrieve(self, request, post_id, comment_id):
        pass

    def update(self, request, post_id, comment_id):
        pass

    def partial_update(self, request, post_id, comment_id):
        pass

    def delete(self, request, post_id, comment_id):
        pass
