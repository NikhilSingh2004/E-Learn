from django.contrib import admin
from courses.models import Course
from courses.models import Topic


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date']

@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'slug']

