
function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('http://127.0.0.1:8000/user_service/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Błąd logowania');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('loginMessage').textContent = 'Zalogowano pomyślne!';
        console.log('Token:', data.access_token);
    })
    .catch(error => {
        document.getElementById('loginMessage').textContent = 'Niepoprawny login lub hasło';
        console.error('Error:', error);
    });
}

