async function validateForm(event) {
    event.preventDefault(); // Impede o envio do formulário

    let username = document.getElementById("usuario").value;
    let password = document.getElementById("senha").value;

    // Limpa a mensagem de erro anterior
    document.getElementById("loginError").textContent = "";

    // Validação simples no frontend: verifica se os campos estão preenchidos
    if (username.trim() === "" || password.trim() === "") {
        document.getElementById("loginError").textContent = "Usuário e senha são obrigatórios.";
        return;  // Não envia os dados para o backend
    }

    // Aqui você pode adicionar mais validações (como verificar o formato do email, etc)

    // Enviar dados para o backend somente se as validações forem passadas
    try {
        let response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        let data = await response.json();

        // Exibe mensagem de erro ou sucesso com base na resposta do backend
        if (data.error) {
            document.getElementById("loginError").textContent = data.error;
        } else {
            // Login bem-sucedido, redireciona ou mostra mensagem
            document.getElementById("loginError").textContent = data.message;
            window.location.href = '/dashboard';  // Exemplo de redirecionamento
        }
    } catch (error) {
        document.getElementById("loginError").textContent = "Erro ao conectar com o servidor.";
    }
}