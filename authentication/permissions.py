from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "patient")

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "patient") and hasattr(obj, "patient"):
            return request.user.patient == obj.patient
        return False


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "doctor")
