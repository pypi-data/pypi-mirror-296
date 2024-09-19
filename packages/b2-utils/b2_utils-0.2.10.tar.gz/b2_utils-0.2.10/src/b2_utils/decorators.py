import functools as _functools
import warnings as _warnings

from django.db import transaction as _transaction
from django.db.models.signals import post_save as _post_save
from django.dispatch import receiver as _receiver
from django.test.utils import override_settings as _override_settings

__all__ = [
    "post_creation_signal",
    "post_commit_signal",
    "celery_task_debug",
]


def post_creation_signal(sender):
    def decorator(func):
        @_receiver(_post_save, sender=sender)
        def wrapper_func(created, instance, *args, **kwargs):
            if created:
                return func(instance)

            return None

        return wrapper_func

    return decorator


def post_commit_signal(sender):
    def decorator(func):
        @_receiver(_post_save, sender=sender)
        def wrapper_func(*args, **kwargs):
            return _transaction.on_commit(lambda: func(*args, **kwargs))

        return wrapper_func

    return decorator


def multi_receiver(signals, sender):
    """
    This decorator works similarly at default django receiver decorator, but
    it allows to register multiple signals at once.

    Ex::

        @multi_receiver([post_save, post_delete], sender=Foo)
        def my_signal(sender, instance, created, **kwargs):
            pass
    """

    def decorator(func):
        for signal in signals:
            _receiver(signal, sender=sender)(func)

        return func

    return decorator


def deprecated(reason: str | None = None):
    def decorator(obj):
        if isinstance(obj, type):
            original_init = obj.__init__

            message = f"Class '{obj.__name__}' is deprecated."
            if reason:
                message += f" {reason}"

            @_functools.wraps(original_init)
            def new_init(self, *args, **kwargs):
                _warnings.warn(
                    message,
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                return original_init(self, *args, **kwargs)

            obj.__init__ = new_init
            return obj

        message = f"'{obj.__name__}' is deprecated."
        if reason:
            message += f" {reason}"

        @_functools.wraps(obj)
        def wrapper(*args, **kwargs):
            _warnings.warn(
                message,
                category=DeprecationWarning,
                stacklevel=2,
            )
            return obj(*args, **kwargs)

        return wrapper

    return decorator


celery_task_debug = _override_settings(
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_ALWAYS_EAGER=True,
    BROKER_BACKEND="memory",
)
