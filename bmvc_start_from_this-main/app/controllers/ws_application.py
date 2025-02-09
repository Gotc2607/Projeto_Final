from time import sleep
import random
from socketio import Server
from app.controllers.datbase import Banco 

class Ws_Application:
    def __init__(self, sio):
        self.db = Banco()
        self.sio = sio
        self.crypto_prices = {"BTC": 567.047, "ETH": 15.490, "DOGE": 1.48}

    def atualizar_precos(self):
        while True:
            for moeda in self.crypto_prices:
                self.crypto_prices[moeda] *= (0.99 + random.random() * 0.02)  # Simula variação de preço
            self.sio.emit('atualizar_precos', self.crypto_prices, namespace='/investimentos')
            sleep(1)

    def comprar_moeda(self, data):
        moeda = data.get('moeda')
        quantidade_em_reais = data.get('quantidade')  # Valor em R$

        if moeda == 'BTC':
            preco_btc = ws.crypto_prices.get('BTC', 1)
            quantidade_btc = quantidade_em_reais / preco_btc  # Convertendo R$ para BTC
            aldo_atual = self.db.obter_saldo(data['usuario'])

            if saldo_atual >= quantidade_em_reais:
                self.db.compra_saldo_disponivel(data['usuario'], quantidade_em_reais)  # Deduzir saldo
                self.db.atualizar_carteira(data['usuario'], moeda, quantidade_btc)  # Atualizar quantidade de BTC na carteira
                self.sio.emit('atualizar_carteira', self.db.Obter_carteira_usuario(data['usuario']), room=sid, namespace='/investimentos')
            else:
                self.sio.emit('erro_compra', {'mensagem': 'Saldo insuficiente'}, room=sid, namespace='/investimentos')
        if moeda == 'ETH':
            preco_eth = self.ws.crypto_prices.get('ETH', 1)
            quantidade_eth = quantidade_em_reais / preco_eth  # Convertendo R$ para ETH
            aldo_atual = self.db.obter_saldo(data['usuario'])

            if saldo_atual >= quantidade_em_reais:
                self.db.compra_saldo_disponivel(data['usuario'], quantidade_em_reais)  # Deduzir saldo
                self.db.atualizar_carteira(data['usuario'], moeda, quantidade_eth)  # Atualizar quantidade de BTC na carteira
                self.sio.emit('atualizar_carteira', self.db.Obter_carteira_usuario(data['usuario']), room=sid, namespace='/investimentos')
            else:
                self.sio.emit('erro_compra', {'mensagem': 'Saldo insuficiente'}, room=sid, namespace='/investimentos')
        if moeda == 'DOGE':
            preco_doge = self.ws.crypto_prices.get('DOGE', 1)
            quantidade_doge = quantidade_em_reais / preco_doge  # Convertendo R$ para DOGE
            aldo_atual = self.db.obter_saldo(data['usuario'])

            if saldo_atual >= quantidade_em_reais:
                self.db.compra_saldo_disponivel(data['usuario'], quantidade_em_reais)  # Deduzir saldo
                self.db.atualizar_carteira(data['usuario'], moeda, quantidade_doge)  # Atualizar quantidade de BTC na carteira
                self.sio.emit('atualizar_carteira', self.db.Obter_carteira_usuario(data['usuario']), room=sid, namespace='/investimentos')
            else:
                self.sio.emit('erro_compra', {'mensagem': 'Saldo insuficiente'}, room=sid, namespace='/investimentos')
    def atualizar_valores_convertidos(self, usuario):
        while True:
            # Atualiza os valores a cada 30 segundos, por exemplo
            self.atualizar_valores(usuario)
            time.sleep(1)
    def atualizar_valores(self, usuario):
        # Obter a carteira do usuário (quantidade de cada moeda)
        carteira = self.model.Obter_carteira_usuario(usuario)
        
        # Preço das criptomoedas (provavelmente um dicionário de preços atualizados)
        preco_btc = self.crypto_prices.get("BTC", 1)
        preco_eth = self.crypto_prices.get("ETH", 1)
        preco_doge = self.crypto_prices.get("DOGE", 1)
        
        # Quantidade das moedas no portfólio do usuário
        quantidade_btc = carteira.get("BTC", 0)
        quantidade_eth = carteira.get("ETH", 0)
        quantidade_doge = carteira.get("DOGE", 0)
        
        # Calculando o valor total de cada moeda em USD (ou outra moeda base)
        valor_btc = quantidade_btc / preco_btc
        valor_eth = quantidade_eth / preco_eth
        valor_doge = quantidade_doge / preco_doge
        
        # Emite a atualização de valores convertidos via WebSocket
        self.sio.emit('atualizar_valores_convertidos', {
            'valor_btc': valor_btc,
            'valor_eth': valor_eth,
            'valor_doge': valor_doge
        }, namespace='/investimentos')

    def atualizar_carteira(self,data):
        usuario = data['usuario']
        carteira = self.db.Obter_carteira_usuario(usuario)  # Pegando os ativos atualizados do usuário
    
        self.sio.emit('carteira_atualizada', carteira, room=request.sid)