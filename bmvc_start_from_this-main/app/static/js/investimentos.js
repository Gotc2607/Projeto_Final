const ws = new WebSocket("ws://localhost:8080/ws/investimentos");

        // Quando o WebSocket estiver aberto, envia uma mensagem de saudação
        ws.onopen = function(event) {
            console.log("Conectado ao WebSocket!");
            // Enviar uma mensagem de exemplo, caso queira, ou aguardar ações do usuário
            // ws.send(JSON.stringify({type: "update", message: "Conectado ao WebSocket!"}));
        };

        // Quando uma mensagem for recebida do servidor
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);  // Receber dados no formato JSON
            if (data.type === 'update') {
                // Atualizar o conteúdo da página com base na mensagem recebida
                alert(data.message);  // Exemplo: Mostrar a mensagem de atualização
            } else if (data.type === 'error') {
                alert(data.message);  // Exemplo: Exibir mensagem de erro
            }
        };

        // Enviar transação de compra/venda
        function realizarTransacao(usuario, crypto, amount, action) {
            const data = {
                type: "trade",
                user_id: usuario,
                crypto: crypto,
                amount: amount,
                action: action
            };
            ws.send(JSON.stringify(data));  // Envia a transação para o servidor
        }

async function obterPrecoCripto(crypto) {
    const url = `https://api.coingecko.com/api/v3/simple/price?ids=${crypto}&vs_currencies=usd`;
    try {
        const response = await fetch(url);
        const data = await response.json();
                
        console.log(data);  // Verifique a resposta da API
                
        if (data[crypto] && data[crypto].usd) {
            const price = data[crypto].usd;
            return price;
        } else {
            throw new Error("Preço não encontrado");
        }
    } catch (error) {
        console.error("Erro ao obter preço: ", error);
        return null;  // Retorna null se houver erro
    }
}

// Exemplo de uso
obterPrecoCripto('BTC').then(price => {
    console.log('Preço do Bitcoin:', price);
});

async function atualizarPrecos() {
    const cryptos = ['BTC', 'ETH', 'LTC'];  // Exemplo de criptomoedas
    const listaPrecos = document.getElementById('precos-criptos'); // Div ou lista onde os preços serão exibidos
    
    // Limpar a lista antes de adicionar os novos preços
    listaPrecos.innerHTML = '';

    for (let i = 0; i < cryptos.length; i++) {
        const crypto = cryptos[i];
        const preco = await obterPrecoCripto(crypto);
        
        if (preco) {
            const item = document.createElement('li');
            item.textContent = `${crypto}: $${preco.toFixed(2)}`;
            listaPrecos.appendChild(item);
        } else {
            const item = document.createElement('li');
            item.textContent = `${crypto}: Não disponível`;
            listaPrecos.appendChild(item);
        }
    }
}

// Chamar a função para atualizar os preços na página
atualizarPrecos();

setInterval(atualizarPrecos, 60000);
