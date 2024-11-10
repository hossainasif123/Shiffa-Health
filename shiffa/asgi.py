
# pet/asgi.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import doctor.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiffa.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                doctor.routing.websocket_urlpatterns  # WebSocket URLs from the doctor app
            )
        )
    ),
})

