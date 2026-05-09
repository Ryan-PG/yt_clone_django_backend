from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Video, Comment
from .serializers import VideoSerializer, VideoCreateSerializer, CommentSerializer

class VideoDetailView(generics.RetrieveAPIView):
    """Get single video details"""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if this video has been viewed in this session
        session_key = f'viewed_video_{instance.id}'
        
        if not request.session.get(session_key, False):
            # Only increment if not viewed in this session
            instance.views_count += 1
            instance.save()
            # Mark as viewed in this session
            request.session[session_key] = True
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class VideoListView(generics.ListAPIView):
    """List all videos (public feed)"""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Add this line to disable pagination

# Add this decorator to exempt CSRF
@method_decorator(csrf_exempt, name='dispatch')
class VideoCreateView(generics.CreateAPIView):
    """Upload new video"""
    serializer_class = VideoCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

class UserVideoListView(generics.ListAPIView):
    """List videos by specific user"""
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Video.objects.filter(uploader_id=user_id)

class CommentListView(generics.ListCreateAPIView):
    """List and create comments for a video"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        video_id = self.kwargs['video_id']
        return Comment.objects.filter(video_id=video_id)
    
    def perform_create(self, serializer):
        video = get_object_or_404(Video, id=self.kwargs['video_id'])
        serializer.save(user=self.request.user, video=video)