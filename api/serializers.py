from rest_framework import serializers
from .models import StorageLocation, Course, CourseStop, CourseRecommender, LuggageBooking


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
    recommender_summary = serializers.SerializerMethodField()
    
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
            "recommender_summary",
        ]

    def get_storage(self, obj):
        storage = obj.storage
        if not storage:
            return None
        return {
            "id": storage.id,
            "name": storage.name,
        }
    
    def get_recommender_summary(self, obj):
        """코스 추천자 요약 데이터(상단 배너 + 바텀시트용)"""

        qs = obj.recommenders.all()  # related_name="recommenders" 기준
        total = qs.count()

        if total == 0:
            return {
                "total_count": 0,
                "representative": None,
                "similar_travelers": [],
                "similar_travelers_extra_count": 0,
            }

        # 대표 추천자: is_representative=True가 있으면 그 사람, 없으면 첫 번째
        primary = qs.filter(is_representative=True).first() or qs.first()

        # 유사 여행자 미니 프로필: 대표 제외 최대 3명
        similar_qs = qs.exclude(pk=primary.pk) if primary else qs
        similar_list = list(similar_qs[:3])

        # +N (extra count) 계산
        if primary:
            extra_count = max(0, total - (1 + len(similar_list)))
        else:
            extra_count = max(0, total - len(similar_list))

        return {
            "total_count": total,
            "representative": CourseRecommenderSerializer(
                primary, context=self.context
            ).data if primary else None,
            "similar_travelers": CourseRecommenderMiniSerializer(
                similar_list, many=True, context=self.context
            ).data,
            "similar_travelers_extra_count": extra_count,
        }

class CourseRecommenderMiniSerializer(serializers.ModelSerializer):
    """상단 배너/유사 여행자 아바타용 최소 정보"""

    class Meta:
        model = CourseRecommender
        fields = [
            "id",
            "name",
            "avatar_url",
            "country_flag_emoji",
        ]


class CourseRecommenderSerializer(serializers.ModelSerializer):
    """대표 추천자 바텀시트에서 사용할 상세 정보"""

    class Meta:
        model = CourseRecommender
        fields = [
            "id",
            "name",
            "avatar_url",
            "country_flag_emoji",
            "visited_text",
            "bio",
            "routes_count",
            "cities_count",
            "followers_count",
        ]
        
class LuggageBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LuggageBooking
        fields = "__all__"