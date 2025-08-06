import gettext as gettext_module


class Babel:
    """Minimal Babel-like class for translation handling."""

    def __init__(self, app=None, locale_selector=None):
        global _babel_instance
        _babel_instance = self
        self.app = app
        self.locale_selector = locale_selector or (lambda: app.config.get('BABEL_DEFAULT_LOCALE', 'en') if app else 'en')
        if app is not None:
            self.init_app(app)

    def init_app(self, app, locale_selector=None):
        self.app = app
        if locale_selector is not None:
            self.locale_selector = locale_selector
        app.config.setdefault('BABEL_DEFAULT_LOCALE', 'en')
        app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', 'translations')


def gettext(message):
    """Fetch translation for the current locale."""
    locale = 'en'
    if _babel_instance and callable(_babel_instance.locale_selector):
        try:
            locale = _babel_instance.locale_selector()
        except Exception:
            locale = 'en'

    translations_dir = 'translations'
    if _babel_instance and getattr(_babel_instance, 'app', None):
        translations_dir = _babel_instance.app.config.get('BABEL_TRANSLATION_DIRECTORIES', 'translations')

    try:
        translation = gettext_module.translation('messages', localedir=translations_dir, languages=[locale])
        return translation.gettext(message)
    except Exception:
        return message


_babel_instance = None

__all__ = ['Babel', 'gettext']

