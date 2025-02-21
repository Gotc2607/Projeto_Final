const socket = io("/investimentos");

        function atualizarPrecos(precoBTC, precoETH, precoDOGE) {
            document.getElementById("precos").innerHTML = `
                <li>BTC: $${precoBTC.toFixed(2)}</li>
                <li>ETH: $${precoETH.toFixed(2)}</li>
                <li>DOGE: $${precoDOGE.toFixed(2)}</li>
            `;
        }

        function atualizarCarteira(carteira) {
            document.getElementById("carteira").innerHTML = `
                <li>BTC: ${carteira.BTC ? carteira.BTC.toFixed(3) : 0}</li>
                <li>ETH: ${carteira.ETH ? carteira.ETH.toFixed(3) : 0}</li>
                <li>DOGE: ${carteira.DOGE ? carteira.DOGE.toFixed(3) : 0}</li>
            `;
        }

        function realizarOperacao(operacao) {
            const moeda = document.getElementById("cripto_moeda").value;
            const quantidade = parseFloat(document.getElementById("quantidade").value);

            if (isNaN(quantidade) || quantidade <= 0) {
                alert("Digite uma quantidade válida.");
                return;
            }

            fetch("/investimentos", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ moeda, quantidade, operacao })
            }).then(res => res.json())
              .then(data => {
                  alert(data.mensagem || data.erro);
                  if (!data.erro) {
                      carregarInvestimentos();
                  }
              })
              .catch(error => console.error("Erro na operação:", error));
        }

        socket.on("atualizar_precos", data => {
            atualizarPrecos(data.preco_btc, data.preco_eth, data.preco_doge);
        });

        socket.on("atualizar_carteira", data => {
            atualizarCarteira(data.carteira);
        });