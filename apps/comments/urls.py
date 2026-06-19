from django.urls import path
from apps.comments.views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path("posts/<slug:slug>/comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
]
