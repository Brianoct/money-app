from django.utils import translation
import logging

logger = logging.getLogger(__name__)

class ForceLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the language from the session
        lang = request.session.get('django_language', 'es')
        logger.info(f"Forcing language to: {lang}")
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        logger.info(f"Active language after forcing: {translation.get_language()}")
        response = self.get_response(request)
        return response