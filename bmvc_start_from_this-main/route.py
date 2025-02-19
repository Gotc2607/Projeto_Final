from app.controllers.application import Application
from app.controllers.ws_application import Ws_Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response
import socketio
from threading import Thread
import eventlet
import eventlet.wsgi


app = Bottle()

 # Inicialização do WebSocket
sio = socketio.Server(async_mode='eventlet')

ws = Ws_Application(sio)
ctl = Application(sio)

sio_app = socketio.WSGIApp(sio, app) 

Thread(target=ws.atualizar_precos, daemon=True).start()

#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/login', method=['GET', 'POST']) #navegador acessa localhost:8080/
def login(info= None):
    return ctl.render('login')

@app.route('/usuario', method=['GET', 'POST'])
def usuario(info= None):
        return ctl.render('usuario')

@app.route('/cadastro', method=['GET', 'POST'])
def cadastro(info= None):
    return ctl.render('cadastro')

@app.route('/deposito', method=['GET', 'POST'])
def deposito(info= None):
    return ctl.render('deposito')

@app.route('/perfil', method=['GET', 'POST'])
def perfil(info=None):
    return ctl.render('perfil') 

@app.route('/fatura', method=['GET', 'POST'])
def fatura(info=None):
    return ctl.render('fatura')

@app.route('/extrato')
def extrato(info=None):
    return ctl.render('extrato')

@app.route('/transferencia', method=['GET', 'POST'])
def transferencia(info=None):
    return ctl.render('transferencia')

@app.route('/pagamento', method=['GET', 'POST'])
def pagamentos(info= None):
    return ctl.render('pagamentos')

@app.route('/pagar_fatura', method=['GET', 'POST'])
def pagar_fatura(info=None):
    return ctl.render('pagar_fatura')

@app.route('/cartão')
def pagina_cartao(info=None):
    return ctl.render('pagina_cartao')

@app.route('/logout')
def logout():
    return ctl.logout()

#-----------------------------------------------------------------------------
#area de investimentos

@app.route('/investimentos', method=['GET', 'POST'])
def investimentos():
    return ctl.render('investimentos')

@app.route('/comprar', method=['POST'])
def comprar():
    response_data = ws.comprar()
    return response.json(response_data)


# WebSocket - Atualizações de Investimentos
@sio.on('connect', namespace='/investimentos')
def conectar(sid, environ):
    print(f'Usuário conectado ao WebSocket: {sid}')
    
    # Emite os preços das criptos na hora da conexão
    sio.emit('atualizar_precos', ws.crypto_prices, room=sid, namespace='/investimentos')
    
    # Emite a carteira inicial para o usuário
    usuario_atual = 'usuario_atual'  # Este valor pode vir do session_id ou de alguma outra forma
    carteira_atualizada = ws.Obter_carteira_usuario(usuario_atual)
    sio.emit('atualizar_carteira', carteira_atualizada, room=sid, namespace='/investimentos')

@sio.on('comprar_moeda', namespace='/investimentos')
def comprar_moeda(sid, data):
    print(f'Comprar moeda com dados: {data}')
    
    usuario = data.get('usuario')
    moeda = data.get('moeda')
    quantidade = data.get('quantidade')
    
    if not usuario or not moeda or not quantidade:
        print("Dados incompletos")
        return
    
    # Realiza a compra da moeda e emite as atualizações necessárias
    ws.comprar_moeda(data, sid)
    carteira_atualizada = ws.Obter_carteira_usuario(usuario)
    
    # Emite a carteira atualizada para o cliente após a compra
    sio.emit('atualizar_carteira', carteira_atualizada, room=sid, namespace='/investimentos')
    
@sio.on('atualizar_carteira')
def atualizar_carteira(data):
    return ws.atualizar_carteira(data)

#-----------------------------------------------------------------------------

if __name__ == '__main__':

    #db = Application()
   eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), sio_app)
