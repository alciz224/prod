from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrAthorPerm(BasePermission):

    """
    Custom permission to allow anonymous users to read only,
    and authenticated users to create and update/delete if they are the author. 
    """

    def has_permission(self, request, view):
        # Allow anyone to list or retrieve (read-only access)
        if view.action in ['list', 'retrieve']:
            return True
        # Allow authenticated users to create
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow anyone to list or retrieve (read-only access)
        if view.action in ['list', 'retrieve']:
            return True
        # Allow update/delete if the user is the author of the object
        if request.user and request.user.is_authenticated:
            return obj.user == request.user
        return False
