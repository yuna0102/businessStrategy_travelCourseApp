from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class TravelerProfile(models.Model):
    """앱 사용자 기본 프로필 (국가, 나이 등)"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default="en")

    def __str__(self):
        return f"{self.user.username} ({self.country})"

#짐 보관소(사이즈별 가격, 보관소 이름, 위치 등)
class StorageLocation(models.Model):
    """짐 보관소/락커 정보"""

    STORAGE_TYPE_CHOICES = [
        ("STATION_LOCKER", "Station Locker"),
        ("CAFE_STORAGE", "Local Storage"),
        ("PRIVATE_STORAGE", "Private Storage"),
    ]
    
    DISTRICT_CHOICES = [
        ("YONGSAN", "Yongsan-gu"),
        ("JONGNO", "Jongno-gu"),
        ("MAPO", "Mapo-gu"),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=STORAGE_TYPE_CHOICES)
    
    district = models.CharField(
        max_length=20,
        choices=DISTRICT_CHOICES,
        default="JONGNO",  # 지역 기본값 설정
    )
    
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    rating = models.FloatField(default=4.5)
    review_count = models.PositiveIntegerField(default=0)

    #사이즈별 시간당 금액 계산 함수
    price_small_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    price_medium_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    price_large_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    open_time_text = models.CharField(max_length=100, blank=True)

    distance_from_center_m = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """특정 보관소 기준 자투리 시간 코스"""

    storage = models.ForeignKey(
        StorageLocation, on_delete=models.CASCADE, related_name="courses"
    )

    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()

    rating = models.FloatField(default=4.5)
    rating_count = models.PositiveIntegerField(default=0)

    thumbnail_url = models.URLField(blank=True)

    created_by_name = models.CharField(max_length=100, blank=True)
    created_by_avatar_url = models.URLField(blank=True)

    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.title} @ {self.storage.name}"


class CourseStop(models.Model):
    """코스 안에 포함된 개별 장소"""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="stops"
    )
    order = models.PositiveIntegerField()

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)

    image_url = models.URLField(blank=True)

    walk_minutes_from_prev = models.PositiveIntegerField(null=True, blank=True)
    distance_from_prev_m = models.PositiveIntegerField(null=True, blank=True)
    stay_minutes = models.PositiveIntegerField(null=True, blank=True)

    rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.name} ({self.course.title})"


class LuggageBooking(models.Model):
    """추후 확장을 위한 예약 정보"""

    traveler = models.ForeignKey(TravelerProfile, on_delete=models.CASCADE)
    storage = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)

    date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)
    dropoff_time = models.TimeField(null=True, blank=True)

    small_count = models.PositiveIntegerField(default=0)
    medium_count = models.PositiveIntegerField(default=0)
    large_count = models.PositiveIntegerField(default=0)

    total_price = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.traveler} @ {self.storage} ({self.date})"

# 코스 추천 프로필 정보   
class CourseRecommender(models.Model):
    """코스를 추천한 실제/가상의 여행자 정보"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="recommenders",
    )

    name = models.CharField(max_length=100)
    avatar_url = models.URLField(blank=True)
    country_flag_emoji = models.CharField(max_length=8, blank=True)

    visited_text = models.CharField(
        max_length=255,
        blank=True,  # ex) "Visited Seoul 3 times in the last 2 years"
    )
    bio = models.TextField(
        blank=True,  # ex) "Backpacker who loves local food markets"
    )

    routes_count = models.PositiveIntegerField(default=0)
    cities_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)

    is_representative = models.BooleanField(
        default=False,  # 대표 추천자로 쓸지 여부
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.course.title}"