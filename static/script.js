document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const passwordStrength = document.getElementById('password-strength');

    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const password = this.value;
            let strength = 0;

            if (password.match(/[a-z]+/)) strength += 1;
            if (password.match(/[A-Z]+/)) strength += 1;
            if (password.match(/[0-9]+/)) strength += 1;
            if (password.match(/[$@#&!]+/)) strength += 1;

            switch (strength) {
                case 0:
                    passwordStrength.style.width = '0%';
                    passwordStrength.style.backgroundColor = '';
                    break;
                case 1:
                    passwordStrength.style.width = '25%';
                    passwordStrength.style.backgroundColor = '#ff4d4d';
                    break;
                case 2:
                    passwordStrength.style.width = '50%';
                    passwordStrength.style.backgroundColor = '#ffa64d';
                    break;
                case 3:
                    passwordStrength.style.width = '75%';
                    passwordStrength.style.backgroundColor = '#99ff99';
                    break;
                case 4:
                    passwordStrength.style.width = '100%';
                    passwordStrength.style.backgroundColor = '#4dff4d';
                    break;
            }
        });
    }

    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function () {
            if (this.value !== passwordInput.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }

   // AJAX form submission
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return response.json();
            } else {
                return response.text();
            }
        })
        .then(data => {
            if (typeof data === 'object') {
                // JSON response
                if (data.success) {
                    showMessage(data.message, 'success');
                    if (data.redirect) {
                        setTimeout(() => {
                            window.location.href = data.redirect;
                        }, 1500);
                    }
                } else {
                    showMessage(data.message, 'error');
                }
            } else {
                // HTML response
                document.open();
                document.write(data);
                document.close();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        });
    });
});
    function showMessage(message, type) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `flash-message ${type}`;
        messageContainer.textContent = message;
        document.querySelector('.container').prepend(messageContainer);
        setTimeout(() => {
            messageContainer.remove();
        }, 5000);
    }
});