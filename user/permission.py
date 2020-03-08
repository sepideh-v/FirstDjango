from rest_framework import permissions


class CustomUpdatePermission(permissions.BasePermission):
    """
    Permission class to check that a user can update his own resource only
    """

    def has_permission(self, request, view):
        # check that its an update request and user is modifying his resource only
        if view.action == 'partial_update' and int(view.kwargs['pk']) != request.user.id:
            return False  # not grant access
        return True  # grant access otherwise
