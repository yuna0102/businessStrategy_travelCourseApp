from rest_framework import serializers
from .models import StorageLocation, Course, CourseStop


#짐 보관소 리스트 정보
class StorageLocationSerializer(serializers.ModelSerializer):
    """보관소 리스트/상세에서 사용할 기본 정보"""

    class Meta:
        model = StorageLocation
        fields = [
            "id",
            "name",
            "type",
            "district",
            "address",
            "rating",
            "review_count",
            "price_small_per_hour",
            "price_medium_per_hour",
            "price_large_per_hour",
            "open_time_text",
            "distance_from_center_m",
        ]


# 코드 카드 내부 요약 정보
class CourseSummarySerializer(serializers.ModelSerializer):
    """코스 리스트(카드)에서 사용할 요약 정보"""

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "summary",
            "duration_minutes",
            "rating",
            "rating_count",
            "thumbnail_url",
            "created_by_name",
            "tags",
        ]

# 코스 상세 페이지 내 카드 정보
class CourseStopSerializer(serializers.ModelSerializer):
    """코스 상세에서 한 개 스팟(카드)"""

    class Meta:
        model = CourseStop
        fields = [
            "id",
            "order",
            "name",
            "description",
            "category",
            "image_url",
            "walk_minutes_from_prev",
            "distance_from_prev_m",
            "stay_minutes",
            "rating",
        ]

#코스 및 스팟 연결 정보
class CourseDetailSerializer(serializers.ModelSerializer):
    """코스 상세 + 스팟 리스트"""

    stops = CourseStopSerializer(many=True, read_only=True)
    storage = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "summary",
            "duration_minutes",
            "rating",
            "rating_count",
            "thumbnail_url",
            "created_by_name",
            "created_by_avatar_url",
            "tags",
            "storage",
            "stops",
        ]

    def get_storage(self, obj):
        return {
            "id": obj.storage.id,
            "name": obj.storage.name,
        }