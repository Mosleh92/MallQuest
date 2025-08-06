import json
import os
from flask import request, session

class Translator:
    def __init__(self, locale_dir='locales', default_locale='en'):
        self.locale_dir = locale_dir
        self.default_locale = default_locale
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        if not os.path.isdir(self.locale_dir):
            return
        for filename in os.listdir(self.locale_dir):
            if filename.endswith('.json'):
                locale = filename.split('.')[0]
                path = os.path.join(self.locale_dir, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)

    def gettext(self, key, locale=None):
        locale = locale or self.default_locale
        return (
            self.translations.get(locale, {}).get(
                key,
                self.translations.get(self.default_locale, {}).get(key, key)
            )
        )

translator = Translator()

def get_locale():
    lang = request.args.get('lang') or session.get('lang') or session.get('language')
    if not lang:
        # Check Accept-Language header
        lang = request.accept_languages.best_match(translator.translations.keys())
    if lang not in translator.translations:
        lang = translator.default_locale
    session['lang'] = lang
    return lang
