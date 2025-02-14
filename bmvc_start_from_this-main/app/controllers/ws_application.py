from time import sleep
from queue import Queue
from bottle import request, response, redirect
import random
from socketio import Server
from app.controllers.datbase import Banco 

class Ws_Application:
    def __init__(self, sio):
        self.db = Banco()
        self.sio = sio
        self.crypto_prices = {"BTC": 567.047, "ETH": 15.490, "DOGE": 1.48}
        self.usuarios_sids = {}
        # Criar uma fila para armazenar os session_id's dos usuários conectados
        self.fila = Queue()
        


    def get_session_id(self):
        """Recupera o session_id do cookie."""
        session_id = request.get_cookie('session_id')
        if not session_id:
            # Se não houver session_id, redireciona para o login
            return redirect('/login')
        return session_id

    def listar_usuarios(self):
        """Obtém todos os usuários e suas carteiras."""
        usuarios = self.db.listar_usuarios()  # Aqui você chama a função para listar todos os usuários
        for usuario in usuarios:
            print(f"Usuário: {usuario[1]}, Email: {usuario[2]}, Saldo: {usuario[3]}")
            # Aqui, você pode enviar dados sobre cada usuário para a interface
            self.sio.emit('atualizar_usuario', {
                'usuario': usuario[1],
                'email': usuario[2],
                'saldo': usuario[3]
            })


    def on_connect(self, sid, environ):
        """Armazena o WebSocket sid associado ao session_id do usuário."""
        query_string = environ.get("QUERY_STRING", "")
        params = dict(param.split("=") for param in query_string.split("&") if "=" in param)
        session_id = params.get("session_id")

        if session_id:
            # Busca o nome do usuário no banco de dados ou na sessão
            usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
            if usuario_autenticado:
                # Armazena o nome do usuário no dicionário junto com o session_id
                self.usuarios_sids[session_id] = dados_usuario.usuario
                self.fila.put(session_id)  # Adiciona session_id na fila
                print(f"Usuário {dados_usuario.usuario} conectado com session_id {session_id}")

    def on_disconnect(self, sid):
        """Remove usuário da fila ao desconectar."""
        session_id_remover = None
        for session_id, usuario_sid in self.usuarios_sids.items():
            if usuario_sid == sid:
                session_id_remover = session_id
                break

        if session_id_remover:
            del self.usuarios_sids[session_id_remover]
            print(f"Usuário {session_id_remover} desconectado")


    def enviar_para_usuario(self, session_id, evento, dados):
        """Envia um evento específico apenas para o usuário correto."""
        sid = self.usuarios_sids.get(session_id)
        if sid:
            self.sio.emit(evento, dados, room=sid)

    def atualizar_precos(self):
        while True:
            # Simula variação de preços
            for moeda in self.crypto_prices:
                self.crypto_prices[moeda] *= (0.99 + random.random() * 0.02)

            while not self.fila.empty():
                session_id = self.fila.get()

                usuario = self.db.obter_usuario_por_session_id(session_id)
                if usuario:
                    self.atualizar_valor_investido(session_id)
                
                    # Atualiza apenas o usuário correto
                    self.sio.emit('atualizar_precos', self.crypto_prices, room=self.usuarios_sids.get(session_id, ''))

            sleep(1)

    def atualizar_valor_investido(self, session_id):
        """Atualiza o valor investido do usuário baseado no preço das criptomoedas."""
        usuario_logado = self.db.obter_usuario_por_session_id(session_id)
    
        if not usuario_logado:
            return  # Se não encontrar o usuário, sai da função

        # Obtém a carteira do usuário logado
        carteira = self.db.Obter_carteira_usuario(usuario_logado)

        # Calcula o valor de cada criptomoeda na carteira
        valor_investido = {
            moeda: carteira.get(moeda, 0) * self.crypto_prices[moeda]
            for moeda in self.crypto_prices
        }

        # Envia os valores atualizados para o WebSocket, caso o usuário esteja conectado
        sid = self.usuarios_sids.get(session_id)
        if sid:
            self.sio.emit('atualizar_valores_convertidos', valor_investido, room=sid)



    def atualizar_valor_invetido(self,session_id):
        usuario_logado = self.db.obter_usuario_por_session_id(session_id)
        
        if not usuario_logado:
            return  # Se não encontrar o usuário, não faz nada

        # Obtém a carteira do usuário logado
        carteira = self.db.Obter_carteira_usuario(usuario_logado)

        # Calcula o valor de cada criptomoeda na carteira
        valor_btc = carteira.get("BTC", 0) * self.crypto_prices["BTC"]
        valor_eth = carteira.get("ETH", 0) * self.crypto_prices["ETH"]
        valor_doge = carteira.get("DOGE", 0) * self.crypto_prices["DOGE"]

        # Envia os valores atualizados para o WebSocket, caso o usuário esteja conectado
        if usuario_logado in self.usuarios_sids:
            self.sio.emit('atualizar_valores_convertidos', {
                'BTC': valor_btc,
                'ETH': valor_eth,
                'DOGE': valor_doge
            }, room=self.usuarios_sids[usuario_logado])

    def comprar_moeda(self, data, sid):
        session_id = data.get('session_id')  # Agora recebemos session_id
        usuario = self.db.obter_usuario_por_session(session_id)  # Busca o usuário associado
        moeda = data.get('moeda')
        quantidade_em_reais = data.get('quantidade')

        preco_atual = self.crypto_prices.get(moeda, 1)
        quantidade_moeda = quantidade_em_reais / preco_atual  # Converte R$ para moeda

        saldo_atual = self.db.obter_saldo(usuario)

        if saldo_atual >= quantidade_em_reais:
            novo_saldo = saldo_atual - quantidade_em_reais
            self.db.compra_saldo_disponivel(usuario, quantidade_em_reais)  # Deduz o saldo
            self.db.atualizar_carteira(usuario, moeda, quantidade_moeda)  # Adiciona à carteira

            # Enviar atualização apenas para o usuário correto
            self.enviar_para_usuario(session_id, 'atualizar_saldo', {'saldo': novo_saldo})
            self.enviar_para_usuario(session_id, 'atualizar_carteira', self.db.Obter_carteira_usuario(usuario))

            return {"mensagem": "Compra realizada com sucesso", "saldo_atualizado": novo_saldo}
        else:
            return {"erro": "Saldo insuficiente"}


    def comprar(self):
        data = request.json
        session_id = data.get("session_id")  
        sid = self.usuarios_sids.get(session_id)

        if not session_id or not data.get('moeda') or not data.get('quantidade'):
            return {"erro": "Dados inválidos"}, 400

        resultado = self.comprar_moeda(data, sid)

        if resultado.get("erro"):
            return resultado, 400
        return {"mensagem": "Compra realizada com sucesso"}


    def atualizar_carteira(self,data):
        session_id = data.get('session_id')  # Agora recebemos session_id
        usuario = self.db.obter_usuario_por_session(session_id)
        carteira = self.db.Obter_carteira_usuario(usuario)  # Pegando os ativos atualizados do usuário
    
        if session_id in self.usuarios_sids:
            sid = self.usuarios_sids[session_id]
            self.sio.emit('carteira_atualizada', carteira, room=sid)