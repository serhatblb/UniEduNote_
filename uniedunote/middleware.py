"""
Global exception logging middleware
Tüm hataları loglar
"""
import logging
from django.http import JsonResponse
from uniedunote.logger_config import get_logger

logger = get_logger('uniedunote')


class GlobalExceptionLoggingMiddleware:
    """
    Tüm exception'ları loglayan middleware
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Exception'ları logla
        """
        logger.error(
            f"Unhandled exception - Path: {request.path}, "
            f"Method: {request.method}, "
            f"User: {request.user.username if request.user.is_authenticated else 'Anonymous'}, "
            f"IP: {self.get_client_ip(request)}, "
            f"Exception: {type(exception).__name__}: {str(exception)}",
            exc_info=True
        )
        return None  # Django'nun default exception handling'ine bırak

    def get_client_ip(self, request):
        """İstemci IP adresini al"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

