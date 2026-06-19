from rest_framework import serializers
from apps.comments.models import Comment


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "author", "body", "created_at")

    def get_author(self, obj):
        return {"id": obj.author.id, "username": obj.author.username}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    replies = ReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id", "post", "author", "parent", "body",
            "is_approved", "reply_count", "replies", "created_at", "updated_at",
        )
        read_only_fields = ("is_approved", "post")

    def get_author(self, obj):
        return {"id": obj.author.id, "username": obj.author.username}

    def get_reply_count(self, obj):
        return obj.replies.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "parent", "body")
