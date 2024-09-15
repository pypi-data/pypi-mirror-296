import os
from django.conf import settings

def ensure_ssl_cert():
    cert_dir = os.path.join(settings.BASE_DIR, 'certificates')
    os.makedirs(cert_dir, exist_ok=True)
    
    certfile = os.path.join(cert_dir, 'cert.pem')
    keyfile = os.path.join(cert_dir, 'key.pem')
    
    if not (os.path.exists(certfile) and os.path.exists(keyfile)):
        os.system(f'openssl req -x509 -newkey rsa:4096 -keyout {keyfile} -out {certfile} -days 365 -nodes -subj "/CN=localhost"')
    
    return certfile, keyfile