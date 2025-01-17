from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response
from app.controllers.controller import Controller


app = Bottle()
ctl = Controller()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>') # rota que está enviando um arquivo css 
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/login', method=['GET','POST'])
def login(info= None):
    return ctl.realizar_login()

#-----------------------------------------------------------------------------



if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
