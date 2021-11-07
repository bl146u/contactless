import json
import string
import random

from channels.db import database_sync_to_async
from django.utils.crypto import constant_time_compare
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import (
    _get_backends,
    authenticate,
    get_user_model,
    SESSION_KEY,
    BACKEND_SESSION_KEY,
    HASH_SESSION_KEY,
)

from apps.ws.mixins import ConsumerMixin
from apps.ws.data import upload_pool


class SignInConsumer(ConsumerMixin):
    group_name = "sign-in"

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
        session.save()
        user_logged_in.send(sender=user.__class__, user=user)

    @database_sync_to_async
    def signin(self, session, username: str, password: str):
        from django.contrib.auth.models import AnonymousUser

        user = authenticate(username=username, password=password)
        if user:
            self.login(session, user)
        else:
            user = AnonymousUser()
        return user

    async def connect(self):
        self.channel_name = "".join(random.sample(string.ascii_lowercase, 16))
        await super().connect()

    async def receive_json(self, content, **kwargs):
        session = self.scope.get("session")
        user = await self.signin(
            session=session,
            username=content.get("username"),
            password=content.get("password"),
        )
        self.scope["session"] = session
        self.scope["user"] = user
        await self.send(
            text_data=json.dumps(
                {
                    "sessionid": session.session_key,
                    "expires": session.get_session_cookie_age(),
                }
            )
        )
        await self.close()


class SignOutConsumer(ConsumerMixin):
    group_name = "sign-out"

    def logout(self, session, user):
        if not user.is_authenticated:
            return
        user_logged_out.send(sender=user.__class__, user=user)
        session.flush()
        session.save()

    @database_sync_to_async
    def signout(self, session):
        from django.contrib.auth.models import AnonymousUser

        self.logout(session, self.scope.get("user"))
        return AnonymousUser()

    async def connect(self):
        self.channel_name = "".join(random.sample(string.ascii_lowercase, 16))
        await super().connect()

    async def receive_json(self, content, **kwargs):
        session = self.scope.get("session")
        user = await self.signout(session)
        self.scope["session"] = session
        self.scope["user"] = user
        await self.send(text_data=json.dumps({}))
        await self.close()


class SignUpConsumer(ConsumerMixin):
    group_name = "sign-up"

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
        session.save()
        user_logged_in.send(sender=user.__class__, user=user)

    def create_user(self, username, password):
        user = get_user_model().objects.create(username=username)
        user.set_password(password)
        user.save()

    @database_sync_to_async
    def signup(self, session, username: str, password: str):
        from django.contrib.auth.models import AnonymousUser

        self.create_user(username, password)
        user = authenticate(username=username, password=password)
        if user:
            self.login(session, user)
        else:
            user = AnonymousUser()
        return user

    async def connect(self):
        self.channel_name = "".join(random.sample(string.ascii_lowercase, 16))
        await super().connect()

    async def receive_json(self, content, **kwargs):
        session = self.scope.get("session")
        user = await self.signup(
            session=session,
            username=content.get("username"),
            password=content.get("password"),
        )
        self.scope["session"] = session
        self.scope["user"] = user
        await self.send(
            text_data=json.dumps(
                {
                    "sessionid": session.session_key,
                    "expires": session.get_session_cookie_age(),
                }
            )
        )
        await self.close()


class SendConsumer(ConsumerMixin):
    group_name = "chat"
    channel_name = "base"

    async def receive_json(self, content, **kwargs):
        data = {
            "name": self.scope.get("user").username,
            "message": content.get("message"),
        }
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat_message", **data},
        )

    async def chat_message(self, event):
        event.pop("type")
        await self.send(text_data=json.dumps(event))


class FilesConsumer(ConsumerMixin):
    group_name = "files"

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        user = self.scope.get("user")
        data = {"user": user.username}
        if bytes_data:
            data = bytes_data.split(b"\n")
            uuid = data.pop()
            data = b"\n".join(data)
            file = upload_pool.write(uuid.decode("utf-8"), data)
            data = file.dict(exclude={"path"})
            if file.size == file.total:
                upload_pool.delete(file)
        else:
            text_data_json = json.loads(text_data)
            data.update(
                {
                    "name": text_data_json.get("name"),
                    "total": text_data_json.get("size"),
                }
            )
            file = upload_pool.create(**data)
            data = {
                "uuid": text_data_json.get("uuid"),
                **file.dict(exclude={"path"}),
            }
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "file_send", **data},
        )

    async def file_send(self, event):
        event.pop("type")
        await self.send(text_data=json.dumps(event))
