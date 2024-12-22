const correctItems = document.getElementsByClassName('correct-section') // находит все кнопки
const correct_csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

for (let item of correctItems) {
    const button = item.querySelector('.correct-check');
    const itemId = button?.getAttribute('data-id'); //если data-id null, то благодаря ? не будет ошибки
    // Определяем тип(если в дальнейшем сюда же добавить обработку нового типа)
    const type = button?.getAttribute('data-type');

    button.addEventListener('click', () => {
        const isChecked = button.checked;
        let url = '';
        if (type == 'correct') {
            url = `/answer/${itemId}/mark_correct/`;
        }
        const request = new Request(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': correct_csrfToken // Добавляем CSRF токен
            },
            body: JSON.stringify({id: itemId}),

        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                button.checked = data.is_correct;
                })
    })
};