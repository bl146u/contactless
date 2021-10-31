"""
ASGI config for apps project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.urls import resolve
from django.core.asgi import get_asgi_application

from config.websocket import WebSocket


def wrapper(app):
    async def asgi(scope, receive, send):
        if scope.get("type") == "websocket":
            match = resolve(scope.get("raw_path"))
            await match.func(
                WebSocket(scope, receive, send), *match.args, **match.kwargs
            )
            return
        await app(scope, receive, send)

    return asgi


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = wrapper(get_asgi_application())
