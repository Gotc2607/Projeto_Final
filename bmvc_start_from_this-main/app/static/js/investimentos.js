// Conectar o socket na inicialização
var socket;

document.addEventListener("DOMContentLoaded", function() {

    const sessionId = getSessionIdFromCookies();  // Pegue o session_id do usuário
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
        document.getElementById('btc_value').innerText = data.valor_btc.toFixed(2);
        document.getElementById('eth_value').innerText = data.valor_eth.toFixed(2);
        document.getElementById('doge_value').innerText = data.valor_doge.toFixed(2);
    });

    // Atualiza o saldo do usuário
    socket.on('atualizar_saldo', function(data) {
        atualizarSaldoNaInterface(data.usuario, data.moeda, data.quantidade);
    });

    // Atualiza a carteira do usuário
    socket.on('atualizar_carteira', function(data) {
        document.getElementById('btc_balance').innerText = data.BTC;
        document.getElementById('eth_balance').innerText = data.ETH;
        document.getElementById('doge_balance').innerText = data.DOGE;
    });

    // Adiciona evento de clique nos botões de compra
    document.querySelectorAll(".actions button").forEach(button => {
        button.addEventListener("click", function(event) {
            let moeda = this.getAttribute("data-moeda");
            comprarMoeda(event, moeda);
        });
    });
});

// Função para comprar moeda e atualizar saldo
function comprarMoeda(event, moeda) {
    event.preventDefault();

    let quantidadeInputId = "quantidade_" + moeda.toLowerCase();
    let quantidade = parseFloat(document.getElementById(quantidadeInputId).value);

    if (!quantidade || quantidade <= 0) {
        alert("Digite um valor válido para comprar.");
        return;
    }

    let precoAtual = parseFloat(document.getElementById(moeda.toLowerCase() + "_price").innerText);
    let saldoElement = document.getElementById("saldo_usuario");
    let saldoAtual = parseFloat(saldoElement.innerText);

    let custoTotal = quantidade;

    // Verifica se o usuário tem saldo suficiente
    if (saldoAtual < custoTotal) {
        alert("Saldo insuficiente para essa compra.");
        return;
    }

    // Atualiza o saldo imediatamente na interface
    let novoSaldo = saldoAtual - custoTotal;
    saldoElement.innerText = novoSaldo.toFixed(2);

    // Envia requisição para comprar
    fetch('/comprar', {
        method: 'POST',
        body: JSON.stringify({ usuario: 'usuario_atual', moeda: moeda, quantidade: quantidade }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.erro) {
            alert("Erro: " + data.erro);
            // Se der erro, restaura o saldo antigo
            saldoElement.innerText = saldoAtual.toFixed(2);
        } else {
            alert("Compra realizada com sucesso!");
            // Atualiza o saldo com o valor vindo do backend (caso precise corrigir)
            saldoElement.innerText = data.saldo_atualizado.toFixed(2);
        }
    })
    .catch(error => {
        console.error("Erro ao comprar moeda:", error);
        alert("Erro ao comprar moeda.");
        // Se der erro, restaura o saldo antigo
        saldoElement.innerText = saldoAtual.toFixed(2);
    });
}

function getSessionIdFromCookies() {
    let sessionId = document.cookie.split('; ')
        .find(row => row.startsWith('session_id='))
        ?.split('=')[1];

    console.log("Session ID recuperado:", sessionId);
    return sessionId;
}


// Função para atualizar o saldo do usuário na interface
function atualizarSaldoNaInterface(usuario, moeda, quantidade) {
    let saldoElement = document.getElementById("saldo_" + moeda.toLowerCase());
    if (saldoElement) {
        saldoElement.innerText = quantidade;
    }
}