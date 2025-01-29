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
            return True, Usuario(usuario=dados_usuario[2], senha=dados_usuario[3],email=dados_usuario[4], saldo=saldo_formatado, fatura=fatura_formatada, session_id=session_id, investimentos=inv_format), dados_usuario[0]
        return False, None

    def depositar(self, valor, senha, usuario):
        dados_usuario = self.db.obter_dados_usuario(usuario)

        print('validando a senha')
        if self.db.verificar_senha(senha, dados_usuario[3]):
            print('senha validada')
        
            self.db.registrar_deposito(usuario, valor)
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
        print('historico de depositos obtido')
    

    
       