from functools import wraps
from rest_framework import status
from rest_framework.response import Response

def put_method_not_allowed(view_func):
    """Декоратор запрета PUT запроса."""
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        """Функция проверки запроса."""
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view