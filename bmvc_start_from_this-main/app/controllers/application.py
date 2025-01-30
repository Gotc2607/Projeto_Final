from bottle import template, request, redirect, response
from app.models.user_account import UsuarioModel
from time import time
import uuid


class Application():

    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'login': self.login,
            'usuario': self.usuario,
            'cadastro': self.cadastro,
            'deposito': self.deposito,
            'perfil': self.perfil,
            'investimentos': self.investimentos,
            'fatura': self.fatura,
            'extrato': self.extrato
        }
        self.model = UsuarioModel()

    def render(self,page, **kwargs):
       content = self.pages.get(page, self.helper)
       return content(**kwargs)


    def helper(self):
        return template('app/views/html/helper')

    def login(self):
        print("Método login chamado")
        if request.method == 'GET':
            return template('app/views/html/login', time=int(time()))
        
        if request.method == 'POST':
            usuario = request.forms.get('usuario')
            senha = request.forms.get('senha')

            if not usuario or not senha:
                print("Campos obrigatórios não preenchidos")
                return template('app/views/html/login', time=int(time()), erro="Preencha todos os campos.")
            
            
           
            at_usuario, dados = self.model.autenticar_usuario(usuario, senha)

            if at_usuario:
                print("Usuário autenticado com sucesso") 

                response.set_cookie('session_id', dados.session_id, httponly=True, secure=True, max_age=3600)

                return template('app/views/html/tela_usuario', usuario=dados.usuario, email=dados.email, saldo=dados.saldo, fatura=dados.fatura, investimentos=dados.investimentos, time=int(time()))
            else:
                print("Usuário ou senha inválidos")
                return template('app/views/html/login', time=int(time()), erro="Usuário ou senha inválidos.")

    def usuario(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')
        
        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if usuario_autenticado:
            return template('app/views/html/tela_usuario', time=int(time()), usuario=dados_usuario.usuario, email=dados_usuario.email, saldo=dados_usuario.saldo, fatura=dados_usuario.fatura, investimentos=dados_usuario.investimentos)
        
        return redirect('/login')

    def cadastro(self):
        if request.method == 'GET':
            return template('app/views/html/cadastro', time=int(time()))
        if request.method == 'POST':
            usuario = request.forms.get('usuario')
            senha = request.forms.get('senha')
            email = request.forms.get('email')
            
            if self.model.adicionar_usuario(usuario, senha, email):
                redirect('/login')

            else:
                return template('app/views/html/cadastro', time=int(time()), erro="Erro ao cadastrar usuário")
        
    def deposito(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/deposito', time=int(time()))
        
        if request.method == 'POST':
            valor = float(request.forms.get('valor'))
            senha = request.forms.get('senha')
            
            if valor <= 0:
                return template('app/views/html/deposito', time=int(time()), erro="O valor deve ser maior que zero.")
                
            if self.model.depositar(valor, senha, dados_usuario.usuario):
                print(f"Depósito no valor de {valor} realizado com sucesso!")
                return redirect('/usuario') 
            return template('app/views/html/deposito', time=int(time()), erro="Erro ao realizar o depósito.")

    def perfil(self):
        session_id = request.get_cookie('session_id') #pega o cokkie da sessão

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario= self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')
        if request.method == 'GET':
            return template('app/views/html/perfil')

    def investimentos(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')
        if request.method == 'GET':
            return template('app/views/html/investir', investimentos=dados_usuario.investimentos)

    def fatura(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')
        if request.method == 'GET':
            return template('app/views/html/pagar-fatura')
    
    def extrato(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario= self.model.verificar_session_id(session_id)
  

        if not usuario_autenticado:
            return redirect('/login')

        depositos = self.model.transacoes(dados_usuario.usuario)
        print(depositos)
        return template('app/views/html/extrato', usuario=dados_usuario.usuario, saldo=dados_usuario.saldo, fatura=dados_usuario.fatura, depositos=depositos)


    def logout(self):
    # Remove o cookie 'session_id' (invalidando a sessão)
        response.delete_cookie('session_id')
    
    # Redireciona para a página de login
        return redirect('/login')