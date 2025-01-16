document.getElementById("loginForm").addEventListener("submit", function(event) {
    const usuario = document.getElementById("usuario").value;
    const senha = document.getElementById("senha").value;

    if (!usuario || !senha) {
        event.preventDefault();
        alert("Preencha todos os campos!");
    }
});