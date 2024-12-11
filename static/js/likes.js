const items = document.getElementsByClassName('like-section') // находит все кнопки
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

for (let item of items) {
    const [button,, counter] = item.children;
    const itemId = button?.getAttribute('data-id'); //если data-id null, то благодаря ? не будет ошибки
    const type = button?.getAttribute('data-type'); // Определяем тип (вопрос или ответ)

    button.addEventListener('click', () => {
        let url = '';
        if (type === 'question') {
            url = `/question/${itemId}/like/`;
        } else if (type === 'answer') {
            url = `/answer/${itemId}/like/`;
        }

        const request = new Request(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Добавляем CSRF токен
            },
            body: JSON.stringify({'id': itemId}),

        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            })
    })
};
