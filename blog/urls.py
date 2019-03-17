from django.urls import path
from . import views, feeds

app_name = 'blog'

urlpatterns = [
    path('', views.PublicPostIndexView.as_view(), name='top'),
    path('private/', views.PrivatePostIndexView.as_view(), name='private_post_list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('reply/create/<int:pk>/', views.ReplyCreate.as_view(), name='reply_create'),
    path('post/add/', views.PostCreateView.as_view(), name='post_add'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),

    path('ajax/tags/get/', views.ajax_get_tags, name='ajax_get_tags'),
    path('ajax/posts/get/', views.ajax_get_posts, name='ajax_get_posts'),

    path('rss/', feeds.RssLatestPostsFeed(), name='rss'),
    path('atom/', feeds.AtomLatestPostsFeed(), name='atom'),
]
