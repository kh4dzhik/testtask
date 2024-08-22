from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO
        return bool(
            request.user.is_authenticated or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        # TODO
        return bool(
            request.user in obj.course.students or request.user.is_staff
        )

class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
