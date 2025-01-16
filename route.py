from app.controllers.view import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>') # rota que está enviando um arquivo css 
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/index', method=['GET', 'POST']) #rota para o arquivo index
def index(info= None):
     if request.method == 'POST':
        usuario = request.forms.get('usuario')
        senha = request.forms.get('senha')
        
        # Processa o login pelo Controller
        if ctl.verificar_login(usuario, senha):
            return redirect('/usuario')
        else:
            return view.index(erro="Usuário ou senha incorretos!")
        return view.index()

@app.route('/tela_cadastro')
def cadastro(info= None):
    return ctl.cadastro()


#-----------------------------------------------------------------------------
# Suas rotas aqui:



#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
