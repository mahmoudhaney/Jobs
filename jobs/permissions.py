from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Application

class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )

class IsApplicationOwnerOrIsAdmin(BasePermission):
    """
    Post Method  -> Only authenticated Users
    GET, PUT, DELETE  -> Only Application Owner
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user and request.user.is_authenticated and not request.user.is_staff
            )
        else:
            if view.kwargs.get('job_id', None):
                job_id = view.kwargs.get('job_id', None)
                try:
                    application = Application.objects.get(owner=request.user.id, job=job_id)
                    return bool(
                    request.user and request.user.is_authenticated and application
                )
                except Application.DoesNotExist:
                    pass
            else:
                return bool(
                    request.user and request.user.is_authenticated
                )