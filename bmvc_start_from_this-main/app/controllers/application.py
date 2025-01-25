from bottle import template, request, redirect, response
from app.models.user_account import UsuarioModel
from time import time


class Application():

    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'login': self.login,
            'usuario': self.usuario,
            'cadastro': self.cadastro
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
            print("Método GET recebido")
            return template('app/views/html/login', time=int(time()))
        
        if request.method == 'POST':
            print("Método POST recebido")
            usuario = request.forms.get('usuario')
            senha = request.forms.get('senha')

            if not usuario or not senha:
                print("Campos obrigatórios não preenchidos")
                return template('app/views/html/login', time=int(time()), erro="Preencha todos os campos.")
            
            
            print(f"Tentando autenticar o usuário: {usuario}")
            at_usuario, dados = self.model.autenticar_usuario(usuario, senha)
            print(dados)    
            print(at_usuario)
            if at_usuario:
                print("Usuário autenticado com sucesso")
                return template('app/views/html/tela_usuario', usuario=dados.usuario, email=dados.email, saldo=dados.saldo, time=int(time()))
            else:
                print("Usuário ou senha inválidos")
                return template('app/views/html/login', time=int(time()), erro="Usuário ou senha inválidos.")

    def usuario(self):
        if request.method == 'GET':
            return template('app/views/html/tela_usuario', time=int(time()))


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
        
       
    
