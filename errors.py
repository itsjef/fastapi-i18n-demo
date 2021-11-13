# flake8: NOQA
from enum import Enum
from typing import Any


# See: https://docs.python.org/3.8/library/gettext.html#deferred-translations
def N_(message: Any) -> Any:
    return message


class StrEnum(str, Enum):
    pass


class NinjaError(StrEnum):
    __slots__ = "_value_", "code"

    def __new__(cls, template, code):
        obj = str.__new__(cls, template)
        obj._value_ = template
        obj.code = code
        return obj

    PASSWORD_TOO_SHORT = (
        N_("Password must be longer than %(min_length)s characters"),
        "E00073",
    )
    INVALID_USERNAME = (
        N_("Username cannot contain special characters"),
        "E00074",
    )

    def __str__(self):
        return self.value


def main():
    import gettext
    import os

    LOCALES = os.listdir(os.path.join(os.path.dirname(__file__), "translations"))
    locale = os.getenv("LOCALE")

    if locale in LOCALES:
        lang = gettext.translation(
            "messages", localedir="translations", languages=[locale]
        )
        _ = lang.gettext
    else:
        _ = gettext.gettext

    print(_(NinjaError.PASSWORD_TOO_SHORT) % {"min_length": 8})
    print(_(NinjaError.INVALID_USERNAME))
    print(_("Hello World"))

    # Not translated on purpose, the original "Thank you" string will be printed
    print(_("Thank you!"))


if __name__ == "__main__":
    main()
