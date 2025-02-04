from bottle import template, request, redirect, response
from app.models.user_account import UsuarioModel
from time import time
import uuid
import json


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
            'extrato': self.extrato,
            'transferencia': self.transferencia,
            'pagamentos': self.pagamentos,
            'pagar_fatura': self.pagar_fatura,
            'pagina_cartao': self.pagina_cartao
        }
        self.model = UsuarioModel()
        self.ws_clients = set()

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
            return template('app/views/html/perfil',  usuario=dados_usuario.usuario, email=dados_usuario.email, senha=dados_usuario.senha)

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

        depositos, transferencias, pagamentos= self.model.transacoes(dados_usuario.usuario)
        print(depositos, transferencias)
        return template('app/views/html/extrato', usuario=dados_usuario.usuario, saldo=dados_usuario.saldo, fatura=dados_usuario.fatura, depositos=depositos, transferencias=transferencias, pagamentos=pagamentos)

    
    def transferencia(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
             return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/transferencia')

        if request.method == 'POST':
            usuario_receptor = request.forms.get('receptor')
            valor = float(request.forms.get('valor'))
            senha = request.forms.get('senha')
            
            usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)

            if valor <= 0:
                return template('app/views/html/transferencia', time=int(time()), erro="O valor deve ser maior que zero.")

            if self.model.transferencia(usuario_receptor, dados_usuario.usuario, valor, senha ):
                return redirect('/usuario')
            return template('app/views/html/transferencia', time=int(time()), erro="Erro ao realizar a transferencia.")

    def pagamentos(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/pagamento', time=int(time()), saldo=dados_usuario.saldo)

        if request.method == 'POST':
            valor = float(request.forms.get('valor'))
            senha = request.forms.get('senha')
            forma_pagamento = request.forms.get('tipo_pagamento')

            print(f'forma de pagamento {forma_pagamento}')

            if forma_pagamento == 'Cartao':
                if self.model.pagamento_com_cartao(dados_usuario.usuario, senha, valor ):
                    print('pagamento realizado')
                    return redirect('/usuario')
                return template('app/views/html/pagamento', erro='Falha no pagamento', saldo=dados_usuario.saldo )
            
            elif forma_pagamento == 'Saldo':
                if valor > float(dados_usuario.saldo) or valor == 0.0:
                    return template('app/views/html/pagamento', time=int(time()), erro="O valor deve ser maior que zero.", saldo=dados_usuario.saldo)
                if self.model.pagamento_com_saldo(dados_usuario.usuario, senha, valor ):
                    print('pagamento realizado')
                    return redirect('/usuario')
                return template('app/views/html/pagamento', erro='Falha no pagamento',saldo=dados_usuario.saldo )

            return  template('app/views/html/pagamento', erro='Falha no pagamento',saldo=dados_usuario.saldo )
            


    def pagar_fatura(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/pagar-fatura', time=int(time()), fatura=dados_usuario.fatura,saldo=dados_usuario.saldo)


        if request.method == 'POST':
            valor = float(request.forms.get('valor'))
            senha = request.forms.get('senha')
            forma_pagamento = request.forms.get('tipo_pagamento')

            if valor > float(dados_usuario.fatura):
                return template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura,saldo=dados_usuario.saldo, erro='Falha no pagamento')
            if forma_pagamento == 'Cartao':
                if self.model.pagamento_com_cartao(dados_usuario.usuario, senha, valor ):
                    if self.model.pagar_fatura(dados_usuario.usuario, senha, valor):
                        return redirect('/usuario')
                    return template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura,saldo=dados_usuario.saldo, erro='Falha no pagamento' )
                return template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura, saldo=dados_usuario.saldo,erro='Falha no pagamento' )

            elif forma_pagamento == 'Saldo':
                if valor > float(dados_usuario.saldo) or valor == 0.0:
                    return template('app/views/html/pagamento', time=int(time()), erro="O valor deve ser maior que zero.", fatura=dados_usuario.fatura,saldo=dados_usuario.saldo)

                if self.model.pagamento_com_saldo(dados_usuario.usuario, senha, valor ):
                    if self.model.pagar_fatura(dados_usuario.usuario, senha, valor):
                        return redirect('/usuario')
                    return template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura, saldo=dados_usuario.saldo, erro='Falha no pagamento' )
                return template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura,saldo=dados_usuario.saldo, erro='Falha no pagamento' )
            else:
                return  template('app/views/html/pagar-fatura', fatura=dados_usuario.fatura, saldo=dados_usuario.saldo , erro='Falha no pagamento' )

    def pagina_cartao(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')
        return template('app/views/html/cartao', time=int(time()), usuario=dados_usuario.usuario, fatura=dados_usuario.fatura)

    def logout(self):
        response.delete_cookie('session_id')
        return redirect('/login')

#----------------------------------------------------------------------
#area de investimentos 
    def investimentos(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')
        if request.method == 'GET':
            return template('app/views/html/investir', investimentos=dados_usuario.investimentos)

    def ws_investimentos(self,ws):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        self.ws_clients.add(ws)
        try:
            for msg in ws:
                data = json.loads(msg)  # Aqui 'msg' é a mensagem recebida, convertida em JSON

            # Aqui verificamos se o tipo da mensagem é 'trade'
                if data['type'] == 'trade':
                    self.model.processar_trade(data, ws)  # Passa o dicionário 'data' para processar o trade

             # Se desejar, pode adicionar mais tipos de mensagem aqui, como 'update' para enviar atualizações ao cliente
                elif data['type'] == 'update':
                    self.send_to_clients({'type': 'update', 'message': 'Atualização disponível!'})
                    
        except:
            pass
        finally:
            self.ws_clients.remove(ws)