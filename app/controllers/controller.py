from bottle import template, request, redirect
from app.controllers.db.database import banco_de_dados

class Controller:

    def __init__(self):
        self.db = banco_de_dados('database.db')
        self.pages = {
            'helper' : self.helper,
            'login' : self.realizar_login
        }

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        return template('../templates/helper')

    def realizar_login(self): # def para a pagina de cadastro
        if request.method == 'GET':
            return template('login', erro = None) # Renderiza a página de login
        
        
        if request.method == 'POST':
            usuario = request.forms.get('usuario') #receber os dados do formulário do login
            senha = request.forms.get('senha')
            
            # Processa o login e redireciona para a página do usuário
            if self.db.verificar_usuario(usuario, senha):
                return redirect(f'/usuario/{usuario}')  # Redireciona para a página do usuário
            else:
                return template('login', erro="Usuário ou senha incorretos!") #casso o login de errado redireciona para a tela de login novamente
    