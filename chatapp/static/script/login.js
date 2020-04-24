document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#tbUsername').addEventListener('keyup', handleChange);
    document.querySelector('#tbPassword').addEventListener('keyup', handleChange);
});

function handleChange() {
    const username = document.querySelector('#tbUsername').value;
    const password = document.querySelector('#tbPassword').value;

    document.querySelector('#btnLogin').disabled = 
        !(username && password);
}