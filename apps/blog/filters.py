import django_filters
from apps.blog.models import Post


class PostFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    author = django_filters.CharFilter(field_name="author__username")
    tag = django_filters.CharFilter(field_name="tags__slug")
    published_after = django_filters.DateFilter(field_name="published_at", lookup_expr="gte")
    published_before = django_filters.DateFilter(field_name="published_at", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ["status", "author", "tag", "published_after", "published_before"]
