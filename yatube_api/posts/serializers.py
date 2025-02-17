from rest_framework import serializers


from .models import Post, Comment, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'title',
            'slug',
            'description',
            'post',
            '',
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            'pub_date',
            'image',
            'author',
            'text',
            'group',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'author',
            'post',
            'text',
            'created',
        )
