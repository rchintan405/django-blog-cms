from rest_framework import serializers
from apps.blog.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ("id", "name", "slug", "post_count")
        read_only_fields = ("slug",)

    def get_post_count(self, obj):
        return obj.posts.filter(status="published").count()


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = (
            "id", "title", "slug", "excerpt", "cover_image",
            "status", "views", "read_time", "author",
            "tags", "comment_count", "published_at", "created_at",
        )

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "full_name": obj.author.full_name,
        }


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ("content", "updated_at")


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, required=False, source="tags"
    )

    class Meta:
        model = Post
        fields = (
            "id", "title", "slug", "excerpt", "content",
            "cover_image", "status", "tag_ids", "published_at",
        )
        read_only_fields = ("slug",)

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
