from django.core.management.base import BaseCommand
from django.core.asgi import get_asgi_application
from ...server.http3_server import run_server
from ...utils.ssl_utils import ensure_ssl_cert

class Command(BaseCommand):
    help = 'Runs the server with HTTP/3 support'

    def handle(self, *args, **options):
        certfile, keyfile = ensure_ssl_cert()
        asgi_app = get_asgi_application()
        run_server(asgi_app, 'localhost', 8000, certfile, keyfile)