# myproject/middleware.py
from django.conf import settings
from django.utils import translation

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang_code = request.GET.get('lang')
        if lang_code:
            translation.activate(lang_code)
            request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
        else:
            lang_code = request.session.get(settings.LANGUAGE_COOKIE_NAME)
            if lang_code:
                translation.activate(lang_code)
        response = self.get_response(request)
        translation.deactivate()
        return response
