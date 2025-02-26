from app.controllers.datbase import Banco
import uuid
import random
import threading
import time
from time import sleep



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
        self.db.criar_carteira()
        self.crypto_prices = {"BTC": 567047, "ETH": 15498, "DOGE": 1.48}

    def adicionar_usuario(self, usuario, senha, email):
        senha_cripto = self.db.hash_senha(senha)
        session_id = self.db.gerar_session_id(usuario)
        self.db.adicionar_usuario(session_id, usuario, senha_cripto, email)
        return True

    def buscar_carteira(self,usuario):
        carteira = self.db.Obter_carteira_usuario(usuario)

        if not carteira:
            self.db.criar_carteira_usuario(usuario)
            carteira_usuario = self.db.Obter_carteira_usuario(usuario)
            return carteira_usuario
        return carteira

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

    def saldo_para_investimentos(self, usuario, quantidade):# usuario pega dinheira da conta principal e deposita na pagina de investimentos
        saldo = self.db.obter_saldo(usuario)
        if quantidade > saldo:
            return False
        self.db.pagamento_com_saldo(usuario, quantidade)
        self.db.deposito_saldo_disponivel(usuario, quantidade)
        return True
    
    def compra_saldo_disponivel(self, usuario, quantidade): #usuario compra os ativos com o saldo disponivel
        saldo = self.db.obter_saldo_disponivel(usuario)
        if quatidade > saldo:
            return False
        self.db.compra_saldo_disponivel(usuario, quantidade)
        return True

#--------------------------------------------------------------------------
    def obter_precos(self):
        preco_btc = self.crypto_prices["BTC"]
        preco_eth = self.crypto_prices["ETH"]
        preco_doge = self.crypto_prices["DOGE"]

        return preco_btc, preco_eth, preco_doge

    def obter_carteira_usuario(self, usuario):
        carteira = self.db.obter_carteira_usuario(usuario)
        if not carteira:
            self.db.criar_carteira_usuario(usuario)
            carteira = self.db.obter_carteira_usuario(usuario)
            return carteira
        return carteira


    def comprar_ativo(self, usuario, ativo, quantidade):
        carteira = self.obter_carteira_usuario(usuario)
        preco_btc, preco_eth, preco_doge = self.obter_precos()
        if ativo == 'BTC':
            valor = quantidade / preco_btc
            self.db.comprar_btc(usuario, valor)
            self.db.pagamento_com_saldo(usuario, quantidade)
            return True
        elif ativo == 'ETH':
            valor = quantidade / preco_eth
            self.db.comprar_eth(usuario, valor)
            self.db.pagamento_com_saldo(usuario, quantidade)
            return True
        elif ativo == 'DOGE':
            valor = quantidade / preco_doge
            self.db.comprar_doge(usuario, valor)
            self.db.pagamento_com_saldo(usuario, quantidade)
            return True
        return False

    def vender_ativo(self, usuario, ativo, quantidade):
        carteira = self.obter_carteira_usuario(usuario)
        preco_btc, preco_eth, preco_doge = self.obter_precos()
        if ativo == 'BTC':
            valor = quantidade / preco_btc
            self.db.vender_btc(usuario, valor)
            self.db.depositar(quantidade, usuario)
            return True
        elif ativo == 'ETH':
            valor = quantidade / preco_eth
            self.db.vender_eth(usuario, valor)
            self.db.depositar(quantidade, usuario)
            return True
        elif ativo == 'DOGE':
            valor = quantidade / preco_doge
            self.db.vender_doge(usuario, valor)
            self.db.depositar(quantidade, usuario)
            return True
        return False
        
    def atualizar_carteira(self, usuario):
        carteira = self.obter_carteira_usuario(usuario)
        return carteira