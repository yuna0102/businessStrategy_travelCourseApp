from rest_framework import generics
from .models import StorageLocation, Course
from .serializers import (
    StorageLocationSerializer,
    CourseSummarySerializer,
    CourseDetailSerializer,
)


class StorageListAPIView(generics.ListAPIView):
    """
    GET /api/storages/
    짐 보관소 리스트
    """

    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer


class StorageCoursesListAPIView(generics.ListAPIView):
    """
    GET /api/storages/<id>/courses/
    특정 보관소 기준 코스 리스트
    """

    serializer_class = CourseSummarySerializer

    def get_queryset(self):
        storage_id = self.kwargs["pk"]
        qs = Course.objects.filter(storage_id=storage_id)
        duration = self.request.query_params.get("duration")
        if duration:
            # 예: /api/storages/1/courses/?duration=120
            qs = qs.filter(duration_minutes=int(duration))
        return qs


class CourseDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/courses/<id>/
    코스 상세 + 스팟 리스트
    """

    queryset = Course.objects.prefetch_related("stops", "storage")
    serializer_class = CourseDetailSerializer
