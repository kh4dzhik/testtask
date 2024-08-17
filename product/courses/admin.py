from django.contrib import admin

from courses.models import Course, Lesson, Group


# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass