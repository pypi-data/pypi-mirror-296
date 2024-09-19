from gettext import gettext as _

__all__ = ("gettext",)


def gettext(msgid: str) -> str:
    return _(msgid)
