from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "patient")


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "doctor")
