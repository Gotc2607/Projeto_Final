from app.controllers.datbase import Banco 


class Usuario:
    
    def __init__(self, usuario, email, saldo=0.0, fatura=0.0):
        self.usuario = usuario
        self.email = email
        self.saldo = saldo
        self.fatura = fatura


class UsuarioModel:

    def __init__(self):
        self.db = Banco()
        self.db.criar_tabela()

    def adicionar_usuario(self, usuario, senha, email):
        """
        Adiciona um usuário ao banco de dados.
        """
        senha_cripto = self.db.hash_senha(senha)
        self.db.adicionar_usuario(usuario, senha_cripto, email)
        return True

    def autenticar_usuario(self, usuario, senha):
        """
        Verifica se o usuário e senha são válidos.
        """
        dados_usuario = self.db.obter_dados_usuario(usuario) #vai retornar uma tupla com os dados do usuario (id [0], usuario[1], senha[2], email[3], saldo[4])
        if dados_usuario and self.db.verificar_senha(senha, dados_usuario[2]):
            print('verificando senha')
            saldo = self.db.obter_saldo(usuario)
            saldo_formatado = "{:.2f}".format(saldo)
            fatura = self.db.obter_fatura(usuario)
            fatura_formatada = "{:.2f}".format(fatura)
            return True, Usuario(usuario=dados_usuario[1], email=dados_usuario[3], saldo=saldo_formatado, fatura=fatura_formatada)
        return False, None

    def depositar(self, valor, senha, usuario):

        dados = self.db.obter_dados_usuario(usuario)

        if self.db.verificar_senha(senha, dados[2]):
            print('verificando senha para deposito')
            saldo = dados[4]
            saldo_atualizado = saldo + valor
            if self.db.deposito(saldo_atualizado, dados[2]):
                print('deposito realizado')
                return True
       

    
       