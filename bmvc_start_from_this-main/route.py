from app.controllers.application import Application
from app.controllers.ws_application import preco
from bottle import Bottle, route, run, request, static_file, redirect, template, response
import socketio
import json
from threading import Thread
import eventlet
import eventlet.wsgi

app = Bottle()

# Inicialização do WebSocket
sio = socketio.Server(async_mode='eventlet')
ctl = Application(sio)
ws = preco(sio)

sio_app = socketio.WSGIApp(sio, app)

Thread(target=ws.atualizar_precos_periodicamente).start()

#-----------------------------------------------------------------------------#
# Servir arquivos estáticos
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

#-----------------------------------------------------------------------------#
# Rotas principais
@app.route('/login', method=['GET', 'POST'])
def login():
    return ctl.render('login')

@app.route('/usuario', method=['GET', 'POST'])
def usuario():
    return ctl.render('usuario')

@app.route('/cadastro', method=['GET', 'POST'])
def cadastro():
    return ctl.render('cadastro')

@app.route('/deposito', method=['GET', 'POST'])
def deposito():
    return ctl.render('deposito')

@app.route('/perfil', method=['GET', 'POST'])
def perfil():
    return ctl.render('perfil')

@app.route('/fatura', method=['GET', 'POST'])
def fatura():
    return ctl.render('fatura')

@app.route('/extrato')
def extrato():
    return ctl.render('extrato')

@app.route('/transferencia', method=['GET', 'POST'])
def transferencia():
    return ctl.render('transferencia')

@app.route('/pagamento', method=['GET', 'POST'])
def pagamentos():
    return ctl.render('pagamentos')

@app.route('/pagar_fatura', method=['GET', 'POST'])
def pagar_fatura():
    return ctl.render('pagar_fatura')

@app.route('/cartão')
def pagina_cartao():
    return ctl.render('pagina_cartao')

@app.route('/logout')
def logout():
    return ctl.logout()

#-----------------------------------------------------------------------------#
# Página de investimentos
@app.route('/investimentos', method=['GET', 'POST'])
def investimentos():
    return ctl.render('investimentos')


#-----------------------------------------------------------------------------#
# WebSocket - Atualizações de Investimentos
@sio.event
def connect(sid, environ):
    print(f'Cliente conectado: {sid}')

@sio.event
def disconnect(sid):
    print(f'Cliente desconectado: {sid}')

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), sio_app)
