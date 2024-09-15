from django.core.asgi import get_asgi_application

def get_http3_asgi_application():
    django_asgi_app = get_asgi_application()
    
    async def http3_asgi_app(scope, receive, send):
        if scope['type'] == 'http':
            scope['http_version'] = '3'
        return await django_asgi_app(scope, receive, send)
    
    return http3_asgi_app