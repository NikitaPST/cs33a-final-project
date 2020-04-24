document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#tbUsername').addEventListener('keyup', handleChange);
    document.querySelector('#tbPassword').addEventListener('keyup', handleChange);
    document.querySelector('#tbConfirmation').addEventListener('keyup', handleChange);
});

function handleChange() {
    const username = document.querySelector('#tbUsername').value;
    const password = document.querySelector('#tbPassword').value;
    const confirmation = document.querySelector('#tbConfirmation').value;

    document.querySelector('#btnRegister').disabled = 
        !(username && password && confirmation);
}