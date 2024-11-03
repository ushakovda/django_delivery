# common/middlewares/session_middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import UserSession
import uuid

class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_id = request.COOKIES.get('session_id')

        if not session_id:
            session_id = str(uuid.uuid4())
            request.session_id = session_id

        UserSession.objects.update_or_create(session_id=session_id)

        request.session_id = session_id
