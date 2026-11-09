const form = document.getElementById('login_form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    const formJSON = Object.fromEntries(formData);

    try {
        const response = await fetch("http://192.168.111.8:5000/api/login", {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                    'Accept': 'application/json'
            },
            body: JSON.stringify(formJSON)
        });

        if (!response.ok) {
            throw new Error('Error ' + response.status);
        }

        const data = await response.json();
        const data_text = JSON.stringify(data);
        console.log("Good: " + data_text);
	localStorage.setItem("name", formJSON["username"])
	window.location.href = data["home"]

    } catch (error) {
        console.error("Error submitting form: " + error)
    }
});
