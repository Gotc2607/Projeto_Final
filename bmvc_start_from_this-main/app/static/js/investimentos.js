var socket;

document.addEventListener("DOMContentLoaded", function() {
    const sessionId = getSessionIdFromCookies();  // Pegue o session_id do usuário
    if (!sessionId) {
        alert("Sessão expirada. Redirecionando para o login.");
        window.location.href = "/login";  // Redireciona para login se session_id não existir
        return;
    }

    socket = io.connect('http://' + document.domain + ':' + location.port + '/investimentos', {
        query: { session_id: sessionId }  // Envia o session_id para o servidor
    });

    socket.on("connect", function() {
        console.log("Conectado com session_id:", sessionId);
    });

    // Atualiza os preços das criptomoedas
    socket.on('atualizar_precos', function(data) {
        document.getElementById('btc_price').innerText = data.BTC.toFixed(2);
        document.getElementById('eth_price').innerText = data.ETH.toFixed(2);
        document.getElementById('doge_price').innerText = data.DOGE.toFixed(2);
    });

    // Atualiza os valores das criptos convertidos em dinheiro
    socket.on('atualizar_valores_convertidos', function(data) {
        document.getElementById('btc_value').innerText = data.BTC.toFixed(2);
        document.getElementById('eth_value').innerText = data.ETH.toFixed(2);
        document.getElementById('doge_value').innerText = data.DOGE.toFixed(2);
    });

    // Atualiza o saldo do usuário
    socket.on('atualizar_saldo', function(data) {
        document.getElementById("saldo_usuario").innerText = data.saldo.toFixed(2);
    });

    // Atualiza a carteira do usuário
    socket.on('atualizar_carteira', function(data) {
        document.getElementById('btc_balance').innerText = data.BTC.toFixed(6);
        document.getElementById('eth_balance').innerText = data.ETH.toFixed(6);
        document.getElementById('doge_balance').innerText = data.DOGE.toFixed(6);
    });

    // Adiciona evento de clique nos botões de compra
    document.querySelectorAll(".actions button").forEach(button => {
        button.addEventListener("click", function(event) {
            let moeda = this.getAttribute("data-moeda");
            comprarMoeda(event, moeda);
        });
    });
});

// Função para verificar saldo disponível
function verificarSaldoDisponivel(saldoAtual, custoTotal) {
    return saldoAtual >= custoTotal;
}

// Função para comprar moeda e atualizar saldo
function comprarMoeda(event, moeda) {
    event.preventDefault();

    let quantidadeInputId = "quantidade_" + moeda.toLowerCase();
    let quantidade = parseFloat(document.getElementById(quantidadeInputId).value);

    // Validação da quantidade inserida
    if (!quantidade || quantidade <= 0 || quantidade > 1000) {  // Limita a compra para 1000 de cada moeda
        alert("Digite um valor válido para comprar (maior que zero e menor que 1000).");
        return;
    }

    let saldoElement = document.getElementById("saldo_usuario");
    let saldoAtual = parseFloat(saldoElement.innerText);

    let custoTotal = quantidade;  // Valor real da criptomoeda (pode ser ajustado conforme a cotação)

    if (!verificarSaldoDisponivel(saldoAtual, custoTotal)) {
        alert("Saldo insuficiente para essa compra.");
        return;
    }

    let sessionId = getSessionIdFromCookies();

    // Atualiza o saldo imediatamente na interface
    let novoSaldo = saldoAtual - custoTotal;
    saldoElement.innerText = novoSaldo.toFixed(2);

    // Exibe o indicador de carregamento
    let botaoCompra = document.querySelector(`[data-moeda=${moeda}]`);
    botaoCompra.disabled = true;
    botaoCompra.innerText = "Processando...";

    // Envia requisição para comprar
    fetch('/comprar', {
        method: 'POST',
        body: JSON.stringify({ session_id: sessionId, moeda: moeda, quantidade: quantidade }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.erro) {
            alert("Erro: " + data.erro);
            saldoElement.innerText = saldoAtual.toFixed(2);
        } else {
            alert("Compra realizada com sucesso!");
            saldoElement.innerText = data.saldo_atualizado.toFixed(2);
        }
        // Reabilita o botão de compra
        botaoCompra.disabled = false;
        botaoCompra.innerText = `Comprar ${moeda}`;
    })
    .catch(error => {
        console.error("Erro ao comprar moeda:", error);
        alert("Erro ao comprar moeda.");
        saldoElement.innerText = saldoAtual.toFixed(2);
        // Reabilita o botão de compra
        botaoCompra.disabled = false;
        botaoCompra.innerText = `Comprar ${moeda}`;
    });
}

function getSessionIdFromCookies() {
    let sessionId = document.cookie.split('; ')
        .find(row => row.startsWith('session_id='))
        ?.split('=')[1];

    console.log("Session ID recuperado:", sessionId);
    return sessionId;
}
