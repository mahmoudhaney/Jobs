from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )

class IsAuthenticatedOrIsAdmin(BasePermission):
    """
    Safe Methods: Admins
    POST, PUT, DELETE: Users & Admins
    But this is wrong logically, we're gonna fix it later
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and request.user.is_staff or
            request.method not in SAFE_METHODS and
            request.user and
            request.user.is_authenticated
        )