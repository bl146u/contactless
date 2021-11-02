import json
import string
import random

from channels.db import database_sync_to_async
from django.utils.crypto import constant_time_compare
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import (
    _get_backends,
    authenticate,
    get_user_model,
    SESSION_KEY,
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
)

from apps.ws.mixins import ConsumerMixin


class SignInConsumer(ConsumerMixin):
    _channel: str = "sign-in"

    def login(self, session, user, backend=None):
        session_auth_hash = ""
        if hasattr(user, "get_session_auth_hash"):
            session_auth_hash = user.get_session_auth_hash()

        if SESSION_KEY in session:
            if get_user_model()._meta.pk.to_python(session[SESSION_KEY]) != user.pk or (
                session_auth_hash
                and not constant_time_compare(
                    session.get(HASH_SESSION_KEY, ""), session_auth_hash
                )
            ):
                session.flush()
        else:
            session.cycle_key()

        try:
            backend = backend or user.backend
        except AttributeError:
            backends = _get_backends(return_tuples=True)
            if len(backends) == 1:
                _, backend = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument or set the "
                    "`backend` attribute on the user."
                )
        else:
            if not isinstance(backend, str):
                raise TypeError(
                    "backend must be a dotted import path string (got %r)." % backend
                )

        session[SESSION_KEY] = user._meta.pk.value_to_string(user)
        session[BACKEND_SESSION_KEY] = backend
        session[HASH_SESSION_KEY] = session_auth_hash
        # user_logged_in.send(sender=user.__class__, request=request, user=user)

    @database_sync_to_async
    def authenticate(self, session, username: str, password: str):
        from django.contrib.auth.models import AnonymousUser

        user = authenticate(username=username, password=password)
        if user:
            self.login(session, user)
        else:
            user = AnonymousUser()
        return user

    async def connect(self):
        self._group = "".join(random.sample(string.ascii_lowercase, 16))
        await self.channel_layer.group_add(self._group, self._channel)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        user = await self.authenticate(
            session=self.scope.get("session"),
            username=content.get("username"),
            password=content.get("password"),
        )
        print(user)

        await self.send(text_data=json.dumps(content))
        await self.close()


class MainConsumer(ConsumerMixin):
    group_name: str = "tmp"
    channel_name: str = "tmp"

    async def connect(self):
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        name = text_data_json.get("name")
        message = text_data_json.get("message")
        file = text_data_json.get("file")
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "name": name,
                "message": message,
                "file": file,
            },
        )

    async def chat_message(self, event):
        name = event.get("name")
        message = event.get("message")
        file = event.get("file")
        await self.send(
            text_data=json.dumps(
                {
                    "name": name,
                    "message": message,
                    "file": file,
                }
            )
        )
