from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import API.routing
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(API.routing.websocket_url)
    )
})