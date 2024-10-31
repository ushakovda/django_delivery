# common/middlewares/session_middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import UserSession
import uuid

class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_id = request.COOKIES.get('session_id')

        if not session_id:
            session_id = str(uuid.uuid4())
            request.session_id = session_id  # Устанавливаем session_id в атрибут запроса

        # Создаем или обновляем сессию в базе данных
        user_id = request.user.id if request.user.is_authenticated else None
        UserSession.objects.update_or_create(session_id=session_id)

        # Сохраняем session_id в атрибутах запроса
        request.session_id = session_id

    def process_response(self, request, response):
        # Кладем ID сессии в куки только при наличии нового session_id
        if hasattr(request, 'session_id'):
            response.set_cookie('session_id', request.session_id)
        return response
