from bottle import template, request, redirect, response
from app.models.user_account import UsuarioModel
from time import time, sleep
import uuid
import json
import threading
import random


class Application():

    def __init__(self, sio):
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
        self.sio = sio
        self.crypto_prices = {"BTC": 50000, "ETH": 3500, "DOGE": 0.10}  # Preços iniciais simulados

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

    def investimentos(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        # Pegando os ativos do usuário no banco de dados
        carteira = self.model.buscar_carteira(dados_usuario.usuario)


        # Evita KeyError caso o usuário não tenha uma dessas moedas
        quantidade_btc = carteira.get("BTC", 0)
        quantidade_eth = carteira.get("ETH", 0)
        quantidade_doge = carteira.get("DOGE", 0)

        # Obtém os preços das criptomoedas
        preco_btc = self.crypto_prices.get("BTC", 1)
        preco_eth = self.crypto_prices.get("ETH", 1)
        preco_doge = self.crypto_prices.get("DOGE", 1)

        # Calcula o valor total que o usuário tem em cada moeda (quantidade * preço atual)
        valor_btc = quantidade_btc / preco_btc if preco_btc else 0
        valor_eth = quantidade_eth / preco_eth if preco_eth else 0
        valor_doge = quantidade_doge / preco_doge if preco_doge else 0

        #emite uma menssagem dos preços atualizados
        self.sio.emit('atualizar_valores_convertidos', {
        'valor_btc': valor_btc,
        'valor_eth': valor_eth,
        'valor_doge': valor_doge
        }, namespace='/investimentos')

        if request.method == 'GET':
            return template('app/views/html/investir',
                investimentos=dados_usuario.investimentos, 
                usuario=dados_usuario.usuario, 
                saldo=dados_usuario.saldo,
                carteira=carteira,
                precos=self.crypto_prices,
                valor_btc=float(valor_btc),
                valor_eth=float(valor_eth),
                valor_doge=float(valor_doge))
        
        if request.method == 'POST':
            data = request.json
            print("Dados recebidos no POST:", data)
            if not data:
                response.status = 400
                return {"erro": "Requisição inválida"}

            moeda = data.get("moeda")
            quantidade = data.get("quantidade")

            if not moeda or not quantidade:
                response.status = 400
                return {"erro": "Dados incompletos"}

            if self.model.atualizar_carteira(dados_usuario.usuario, moeda, quantidade):
                response.status = 200
                return {"mensagem": f"Compra de {quantidade} em {moeda} realizada com sucesso!"}
            else:
                response.status = 500
                return {"erro": "Erro ao atualizar a carteira."}

    def atualizar_valor_carteira(self, usuario):
        # Recalcular o valor da carteira após a compra
        carteira = self.model.buscar_carteira(usuario)

        # Calcula o valor total das moedas no portfólio do usuário
        quantidade_btc = carteira.get("BTC", 0)
        quantidade_eth = carteira.get("ETH", 0)
        quantidade_doge = carteira.get("DOGE", 0)

        preco_btc = self.crypto_prices.get("BTC", 1)
        preco_eth = self.crypto_prices.get("ETH", 1)
        preco_doge = self.crypto_prices.get("DOGE", 1)

        valor_btc = quantidade_btc / preco_btc if preco_btc else 0
        valor_eth = quantidade_eth / preco_eth if preco_eth else 0
        valor_doge = quantidade_doge / preco_doge if preco_doge else 0

        # Emite a atualização de valores para o WebSocket
        self.sio.emit('atualizar_valores_convertidos', {
            'valor_btc': valor_btc,
            'valor_eth': valor_eth,
            'valor_doge': valor_doge
        }, namespace='/investimentos')