from django.urls import path
from .views_api import CommentListCreateAPIView, LikeToggleAPIView

urlpatterns = [
    path('<int:note_id>/comments/', CommentListCreateAPIView.as_view(), name='note-comments'),
    path('<int:note_id>/like/', LikeToggleAPIView.as_view(), name='note-like'),

]
