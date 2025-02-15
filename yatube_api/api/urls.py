from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import (
    PostsViewSet,
    PostViewSet,
    GroupListCreateViewSet,
    CommentsViewSet,
    CommentViewSet,
)


router = DefaultRouter()

router.register('posts', PostsViewSet)
router.register(
    'posts/<int:post_id>/',
    PostViewSet,
    basename='post'
)
router.register('groups', GroupListCreateViewSet)
router.register(
    'posts/<int:post_id>/comments/<int:comment_id>/',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/posts/<int:post_id>/comments/',
        CommentsViewSet.as_view(),
        name='comments'
    ),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
