def simple_app(environ, start_response):
    """
    Простое WSGI-приложение для обработки GET и POST параметров.
    """
    # Получение метода (GET или POST)
    method = environ['REQUEST_METHOD']
    params = ""

    if method == "GET":
        # Получение строки запроса
        query_string = environ.get('QUERY_STRING', '')
        params = query_string

    elif method == "POST":
        try:
            # Получение длины содержимого и его чтение
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
            params = post_data
        except (ValueError, KeyError):
            params = "Ошибка при обработке POST данных"

    # Подготовка ответа
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    response = f"Метод: {method}\nПараметры:\n{params}".encode('utf-8')
    return [response]
