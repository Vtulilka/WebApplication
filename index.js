document.addEventListener('DOMContentLoaded', () => {
  let url = 'https://awfulevil.pythonanywhere.com/api/users/'
  let data = {username: "user", password: "1234", email: "user@user", first_name: "first", last_name: "last"}
  // Функция для отправки POST-запроса
  const postData = async (url = url, data = data) => {
    // Формируем запрос
    const response = await fetch(url, {
      mode: 'no-cors',

      // Метод, если не указывать, будет использоваться GET
      method: 'POST',
      // Заголовок запроса
      headers: {
        'Content-Type': 'application/json'
      },
      // Данные
      body: JSON.stringify(data)
    });
    console.log(response);
    return response.json();
  }

  // Вызов функции postData при загрузке страницы
  const callPostData = async () => {
    try {
      const result = await postData();
      console.log('Data received:', result);
      const dataContainer = document.getElementById('data-container');
      dataContainer.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
      console.error('Error:', error);
      const dataContainer = document.getElementById('data-container');
      dataContainer.textContent = 'Error: ' + error.message;
    }
  }

  callPostData();
});

