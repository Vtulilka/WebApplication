from rest_framework import permissions

class NotAuthorizedPermission(permissions.BasePermission):
    """
    Разрешения для методов создания/аутентификации пользователя
    """
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            blocked = True
            if 'login' in request.path:
                message = 'User is already authenticated'
            else:
                message = 'Authenticated users cannot create new users.\n Log out and try again'
        else:
            blocked = False
        
        return not blocked
