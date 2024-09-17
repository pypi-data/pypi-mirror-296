# This file is placed in the Public Domain.
# pylint: disable=R0902,R0903,R0911,W0105,W0718


"deferred exception handling"


import traceback


class Errors:

    "Errors"

    errors = []


def formatexc(exc):
    "format an exception"
    res = ""
    ress = traceback.format_exception(
                               type(exc),
                               exc,
                               exc.__traceback__
                              )
    for line in ress:
        res += line
    return res


def errors(outer):
    "display errors."
    for exc in Errors.errors:
        outer(exc)


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    fmt = formatexc(excp)
    if fmt not in Errors.errors:
        Errors.errors.append(fmt)


def __dir__():
    return (
        'Errors',
        'errors',
        'later'
    )
