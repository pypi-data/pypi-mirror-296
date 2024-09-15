# django-http3-package

# Django HTTP/3 Package Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

Django HTTP/3 is a package that enables automatic HTTP/3 support for Django projects. It simplifies the process of adding HTTP/3 capabilities to your Django application, allowing for improved performance and reduced latency for compatible clients.

## Requirements

- Python 3.8+
- Django 3.0+
- OpenSSL (for certificate generation)

## Installation

To install the Django HTTP/3 package, run the following command:

```bash
pip install django-http3
```

## Configuration

1. Add 'django_http3' to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_http3',
]
```

2. Add the HTTP/3 middleware to your MIDDLEWARE in settings.py:

```python
MIDDLEWARE = [
    'django_http3.middleware.HTTP3Middleware',
    ...
]
```

3. Update your asgi.py file to use the HTTP/3 ASGI application:

```python
from django_http3.utils.asgi_utils import get_http3_asgi_application

application = get_http3_asgi_application()
```

4. (Optional) Configure HTTP/3 settings in your settings.py:

```python
HTTP3_HOST = 'localhost'  # Default
HTTP3_PORT = 8000  # Default
```

## Usage

To run your Django server with HTTP/3 support, use the following management command:

```bash
python manage.py runhttp3
```

This command will start the server and automatically generate self-signed SSL certificates if they don't exist.

## Examples

### Basic Usage

Here's a simple example of how to set up a Django project with HTTP/3 support:

1. Create a new Django project:

```bash
django-admin startproject myproject
cd myproject
```

2. Install django-http3:

```bash
pip install django-http3
```

3. Update settings.py:

```python
INSTALLED_APPS = [
    ...
    'django_http3',
]

MIDDLEWARE = [
    'django_http3.middleware.HTTP3Middleware',
    ...
]
```

4. Update asgi.py:

```python
from django_http3.utils.asgi_utils import get_http3_asgi_application

application = get_http3_asgi_application()
```

5. Run the server:

```bash
python manage.py runhttp3
```

### Custom Port

To run the HTTP/3 server on a custom port:

1. Update settings.py:

```python
HTTP3_PORT = 8443
```

2. Run the server:

```bash
python manage.py runhttp3
```

### Production Setup

For production, you should use proper SSL certificates. Update your settings.py:

```python
HTTP3_CERT_FILE = '/path/to/your/certfile.pem'
HTTP3_KEY_FILE = '/path/to/your/keyfile.pem'
```

## Troubleshooting

1. **SSL Certificate Issues**: If you encounter SSL certificate problems, ensure that you have OpenSSL installed and that the certificate files are readable by the application.

2. **Port Already in Use**: If the port is already in use, you can change it in your settings.py file or stop the process using that port.

3. **Compatibility**: Ensure your client supports HTTP/3. Not all browsers have HTTP/3 enabled by default.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.