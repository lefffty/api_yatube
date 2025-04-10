from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views


# router = DefaultRouter()

# router.register('posts', views.PostsViewSet)
# router.register(
#     'posts/<int:post_id>/',
#     views.PostViewSet,
#     basename='post'
# )
# router.register(
#     'groups',
#     views.GroupListCreateViewSet
# )
# router.register(
#     'posts/<int:post_id>/comments/<int:comment_id>/',
#     views.CommentViewSet,
#     basename='comment',
# )

# urlpatterns = [
#     path(
#         'api/v1/',
#         include(router.urls),
#     ),
#     path(
#         'api/v1/posts/<int:post_id>/comments/',
#         views.CommentsViewSet.as_view(),
#         name='comments'
#     ),
#     path(
#         'api/v1/api-token-auth/',
#         obtain_auth_token,
#     ),
# ]

urlpatterns = [
    path(
        'api/v1/api-token-auth/',
        obtain_auth_token,
    ),
    path(
        'api/v1/posts/',
        views.api_posts,
    ),
    path(
        'api/v1/posts/<int:post_id>/',
        views.api_post_detail,
    ),
    path(
        'api/v1/groups/',
        views.api_groups,
    ),
    path(
        'api/v1/groups/<int:group_id>/',
        views.api_group_detail,
    ),
    path(
        'api/v1/posts/<int:post_id>/comments/',
        views.api_comments,
    ),
    path(
        'api/v1/posts/<int:post_id>/comments/<int:comment_id>/',
        views.api_comment_detail,
    ),
]
