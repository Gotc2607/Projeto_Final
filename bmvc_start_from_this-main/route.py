from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
from bottle_websocket import websocket, GeventWebSocketServer


app = Bottle()
ctl = Application()


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
def investimentos(info=None):
    return ctl.render('investimentos')

@app.route('/ws/investimentos', apply=[websocket])
def ws_investimentos(ws):
    ctl.ws_investimentos(ws)

@app.route('/api/saldo_investido', method='GET')
def saldo_investido(info=None):
    return ctl.saldo_investido()


#-----------------------------------------------------------------------------

if __name__ == '__main__':

    db = Application()
    run(app, host='0.0.0.0', port=8080, debug=True ,server=GeventWebSocketServer)
