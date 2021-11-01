from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(session_key=None):
    from django.contrib.auth.models import User, AnonymousUser
    from django.contrib.sessions.models import Session

    if not session_key:
        return AnonymousUser()

    session = Session.objects.filter(session_key=session_key).first()
    if not session:
        return AnonymousUser()

    session_data = session.get_decoded()
    user = User.objects.filter(pk=session_data.get("_auth_user_id")).first()
    if not user:
        return AnonymousUser()

    return user


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        sessionid = scope.get("cookies", {}).get("sessionid")
        scope.update({"user": await get_user(sessionid)})
        return await super().__call__(scope, receive, send)
