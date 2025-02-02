from app.controllers.datbase import Banco
import uuid


class Usuario:
    
    def __init__(self, usuario,senha, email, saldo=0.0, fatura=0.0, session_id=None, investimentos=0.0):
        self.usuario = usuario
        self.senha = senha
        self.email = email
        self.saldo = saldo
        self.fatura = fatura
        self.session_id = session_id
        self.investimentos= investimentos


class UsuarioModel:

    def __init__(self):
        self.db = Banco()
        self.db.criar_tabela1()
        self.db.cria_tabela_depositos()
        self.db.criar_tabela_trades()

    def adicionar_usuario(self, usuario, senha, email):
        senha_cripto = self.db.hash_senha(senha)
        session_id = self.db.gerar_session_id(usuario)
        self.db.adicionar_usuario(session_id, usuario, senha_cripto, email)
        return True

    def autenticar_usuario(self, usuario, senha):
        dados_usuario = self.db.obter_dados_usuario(usuario) #vai retornar uma tupla com os dados do usuario (id [0], session_id[1], usuario[2], senha[3], email[4], saldo[5], fatura[6])
        if dados_usuario and self.db.verificar_senha(senha, dados_usuario[3]):
           
            session_id = self.db.gerar_session_id(usuario) #gerando um sssion_id para o usuario

            saldo = self.db.obter_saldo(usuario)
            saldo_formatado = "{:.2f}".format(saldo)
            fatura = self.db.obter_fatura(usuario)
            fatura_formatada = "{:.2f}".format(fatura)
            investimentos = dados_usuario[7]
            inv_format =  "{:.2f}".format(investimentos)
            return True, Usuario(usuario=dados_usuario[2],senha=dados_usuario[3],email=dados_usuario[4], saldo=saldo_formatado, fatura=fatura_formatada, session_id=session_id, investimentos=inv_format)
        return False, None

    def verificar_session_id(self, session_id):
        usuario = self.db.obter_usuario_por_session_id(session_id)
        
        if usuario:
            dados_usuario = self.db.obter_dados_usuario(usuario)
            saldo = self.db.obter_saldo(usuario)
            saldo_formatado = "{:.2f}".format(saldo)
            fatura = self.db.obter_fatura(usuario)
            fatura_formatada = "{:.2f}".format(fatura)
            investimentos = dados_usuario[7]
            inv_format =  "{:.2f}".format(investimentos)
            print(f"Dados do usuário encontrados: {dados_usuario}") 

            return True, Usuario(usuario=dados_usuario[2], senha=dados_usuario[3],email=dados_usuario[4], saldo=saldo_formatado, fatura=fatura_formatada, session_id=session_id, investimentos=inv_format)

        print("Nenhum usuário encontrado para este session_id.")
        return False, None

    def depositar(self, valor, senha, usuario):
        dados_usuario = self.db.obter_dados_usuario(usuario)

        print('validando a senha')
        if self.db.verificar_senha(senha, dados_usuario[3]):
            print('senha validada')

            tipo = 'deposito'
            self.db.registrar_operacoes(usuario, tipo, valor)
            print('deposito registrado')

            saldo = dados_usuario[5]
            saldo_atualizado = saldo + valor

            if self.db.deposito(saldo_atualizado, usuario):
                print('deposito realizado')
                return True
            return False
        return False
    
    def transacoes(self, usuario_id):
        historico_depositos = self.db.obter_depositos(usuario_id)
        historico_transferencias = self.db.obter_transferencias(usuario_id)
        historico_pagamentos = self.db.obter_pagamentos(usuario_id)
        print('historico de depositos obtido')
        return historico_depositos, historico_transferencias, historico_pagamentos

    def transferencia(self,usuario_receptor, usuario_atual, valor, senha):

        dados = self.db.obter_dados_usuario(usuario_atual)
        if not self.db.verificar_senha(senha, dados[3]):
            return False
        if self.db.verificar_usuario(usuario_receptor):
            if self.db.transferencia(usuario_receptor, usuario_atual, valor, senha):
                tipo1 = 'transferencia'
                self.db.registrar_operacoes(usuario_atual, tipo1, valor)
                tipo2 = 'deposito'
                self.db.registrar_operacoes(usuario_receptor, tipo2, valor )
                return True
            return False
        return False

    def pagamento_com_saldo(self, usuario, senha, valor):
        dados = self.db.obter_dados_usuario(usuario)
        if not self.db.verificar_senha(senha, dados[3]):
            return False
        if self.db.pagamento_com_saldo(usuario, valor):
            tipo = 'pagamento'
            self.db.registrar_operacoes(usuario, tipo, valor)
            return True
        return False

    def pagamento_com_cartao(self, usuario, senha, valor):
        dados = self.db.obter_dados_usuario(usuario)
        if not self.db.verificar_senha(senha, dados[3]):
            return False
        if self.db.pagamento_com_cartao(usuario, valor):
            tipo = 'pagamento'
            self.db.registrar_operacoes(usuario, tipo, valor)
            return True
        return False

    def pagar_fatura(self,usuario, senha, valor):
        dados = self.db.obter_dados_usuario(usuario)
        if not self.db.verificar_senha(senha, dados[3]):
            return False
        if self.db.pagar_fatura(usuario, valor):
            tipo = 'pagamento'
            self.db.registrar_operacoes(usuario, tipo, valor)
            return True
        return False
#--------------------------------------------------------------------------
#area de investimentos

def enviar_para_clientes(self, data):
        for client in self.ws_clients:
            try:
                client.send(json.dumps(data))
            except:
                pass

def processar_trade(self, data, ws):

    user_id = data['user_id']  # Acessa o ID do usuário
    crypto = data['crypto']    # Acessa o nome da criptomoeda
    amount = float(data['amount'])  # Acessa a quantidade de criptomoeda
    action = data['action']    # Acessa a ação ('buy' ou 'sell')


    saldo_investido = self.db.saldo_investido(usuario)
    
    if saldo_investido is None:
        ws.send(json.dumps({'type': 'error', 'message': 'Usuário não encontrado'}))
        return

    if action == "buy":  # COMPRA
        novo_saldo = saldo_investido + amount
    elif action == "sell":  # VENDA
        if saldo_investido < amount:
            ws.send(json.dumps({'type': 'error', 'message': 'Saldo insuficiente'}))
            return
        novo_saldo = saldo_investido - amount
    else:
        ws.send(json.dumps({'type': 'error', 'message': 'Ação inválida'}))
        return

    # Atualizar saldo investido do usuário no banco
    self.db.atualizar_saldo_investido(usuario, novo_saldo)

    # Registrar o trade na tabela de trades
    self.db.registrar_trade(usuario, crypto, quantia, action)

    # Notificar todos os clientes sobre a atualização
    self.enviar_para_clientes({'type': 'update', 'message': f"{usuario} {action} {quantia} {crypto}"})

    

    
       