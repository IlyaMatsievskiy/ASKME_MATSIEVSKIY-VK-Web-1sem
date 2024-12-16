import multiprocessing

# Адрес и порт, на котором будет запущен Gunicorn
bind = "127.0.0.1:8081"

# Количество воркеров
workers = 2

# Указываем путь к вашему WSGI-приложению
wsgi_app = "test_wsgi.simple_wsgi:simple_app"