const senhaReal = "minhaSenha123";

        // Função para exibir a senha ocultada
        function exibirSenhaOcultada() {
            const senhaOcultada = senhaReal.replace(/./g, '•'); // Substitui todos os caracteres por •
            document.getElementById('senha').textContent = senhaOcultada;
        }

        // Função para mostrar a senha real
        function mostrarSenha() {
            document.getElementById('senha').textContent = senhaReal;
        }

        // Exibe a senha ocultada ao carregar a página
        exibirSenhaOcultada();