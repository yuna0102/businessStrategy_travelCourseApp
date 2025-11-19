from django.urls import path
from . import views

urlpatterns = [
    path("storages/", views.StorageListAPIView.as_view(), name="storage-list"),
    path(
        "storages/<int:pk>/courses/",
        views.StorageCoursesListAPIView.as_view(),
        name="storage-courses",
    ),
    path(
        "courses/<int:pk>/",
        views.CourseDetailAPIView.as_view(),
        name="course-detail",
    ),
]