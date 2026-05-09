from django.urls import path
from . import views

urlpatterns = [
    path('', views.VideoListView.as_view(), name='video-list'),
    path('upload/', views.VideoCreateView.as_view(), name='video-upload'),
    path('<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('user/<int:user_id>/', views.UserVideoListView.as_view(), name='user-videos'),
    path('<int:video_id>/comments/', views.CommentListView.as_view(), name='video-comments'),
]