from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyOrIsAuthenticatedOrIsAuthor(BasePermission):
    '''Set user access rights.'''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user == obj.author:
            return True
        return False
