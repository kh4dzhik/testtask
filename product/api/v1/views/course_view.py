from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer,
                                                  CourseAvailableSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    # def get_object(self):
    #     instanse = super().get_object()
    #     if self.request.user in instanse.students.all():
    #         return instanse
    #
        # return HttpResponseForbidden()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available(self, request):
        qs = Course.objects.filter(available_flag=True).exclude(students__in=[self.request.user]).annotate(
            anno_lessons_count=Count('lessons')
        )
        data = CourseAvailableSerializer(qs, many=True).data

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        # TODO

        qs = Course.objects.filter(available_flag=True).exclude(students__in=[self.request.user])

        # если продукт уже куплен, вернет 404
        course = get_object_or_404(qs, id=pk)
        user = self.request.user

        if course.price <= self.request.user.balance.balance:
            Subscription.objects.create(user=user, course=course)
            # course.students.add(user)
            user.balance.balance = user.balance.balance - course.price
            user.balance.save()

        ser = self.get_serializer_class()
        data = ser(course).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


# class CourseAvailableViewList(ListModelMixin, GenericViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = CourseAvailableSerializer
#
#     def get_queryset(self):
#         qs = Course.objects.all()
#         return qs.exclude(students__in=[self.request.user]).annotate(anno_lessons_count=Count('lessons'))
