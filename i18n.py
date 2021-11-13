import os

from babel import Locale
from babel.support import Translations
from starlette_context import context

DEFAULT_LOCALE = Locale.parse("en")
DOMAIN = "messages"
TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), "translations")


def _get_current_context():
    return context if context.exists() else None


def get_locale():
    ctx = _get_current_context()
    if ctx is None:
        return None

    locale = getattr(ctx, "babel_locale", None)
    if locale is None:
        rv = context.data.get(
            "Accept-Languages"
        )  # might add some custom locale selector here, i.e: query from database
        if rv is None:
            locale = DEFAULT_LOCALE
        else:
            locale = Locale.parse(rv)
        setattr(ctx, "babel_locale", locale)

    return locale


def get_translations():
    locale = get_locale()
    # print(locale)

    # might add some caching mechanism here to avoid
    # reloading each time getting a translation
    translations = Translations()
    catalog = Translations.load(TRANSLATIONS_DIR, [locale], DOMAIN)
    translations.merge(catalog)

    if hasattr(catalog, "plural"):
        translations.plural = catalog.plural

    return translations


def gettext(string, **variables):
    t = get_translations()
    s = t.ugettext(string)
    return s if not variables else s % variables


_ = gettext
