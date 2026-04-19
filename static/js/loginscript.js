
// Toggle between login and registration forms
document.addEventListener("DOMContentLoaded", ()=> {
    let registerButton = document.querySelector('#showRegister')
    let loginButton = document.querySelector('#showLogin')
    registerButton.addEventListener('click',()=>{
        
        document.querySelector('#loginForm').classList.add('hidden')
        document.querySelector('#registerForm').classList.remove('hidden')

        document.querySelector('#showRegister').classList.add('hidden')
        document.querySelector('#showLogin').classList.remove('hidden')
    })
    loginButton.addEventListener('click',()=>{
        document.querySelector('#loginForm').classList.remove('hidden')
        document.querySelector('#registerForm').classList.add('hidden')

        document.querySelector('#showRegister').classList.remove('hidden')
        document.querySelector('#showLogin').classList.add('hidden')
    })


});

