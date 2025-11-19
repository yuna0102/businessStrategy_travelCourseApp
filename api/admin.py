from django.contrib import admin
from .models import (
    TravelerProfile,
    StorageLocation,
    Course,
    CourseStop,
    LuggageBooking,
)

admin.site.register(TravelerProfile)
admin.site.register(StorageLocation)
admin.site.register(Course)
admin.site.register(CourseStop)
admin.site.register(LuggageBooking)