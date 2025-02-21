from bottle import template, request, redirect, response
from app.models.user_account import UsuarioModel
from time import sleep, time
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
        self.crypto_prices = {"BTC": 567047, "ETH": 15490, "DOGE": 1.48}  # Preços iniciais simulados
    
    def render(self,page, **kwargs):
       content = self.pages.get(page, self.helper)
       return content(**kwargs)


    def helper(self):
        return template('app/views/html/helper')

    def login(self):
        print("Método login chamado")
        if request.method == 'GET':
            return template('app/views/html/login', t=int(time()))
        
        if request.method == 'POST':
            usuario = request.forms.get('usuario')
            senha = request.forms.get('senha')

            if not usuario or not senha:
                print("Campos obrigatórios não preenchidos")
                return template('app/views/html/login', t=int(time()), erro="Preencha todos os campos.")
            
            
           
            at_usuario, dados = self.model.autenticar_usuario(usuario, senha)

            if at_usuario:
                print("Usuário autenticado com sucesso") 

                response.set_cookie('session_id', dados.session_id, httponly=True, secure=True, max_age=3600)

                return template('app/views/html/tela_usuario', usuario=dados.usuario, email=dados.email, saldo=dados.saldo, fatura=dados.fatura, investimentos=dados.investimentos, t=int(time()))
            else:
                print("Usuário ou senha inválidos")
                return template('app/views/html/login', t=int(time()), erro="Usuário ou senha inválidos.")

    def usuario(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')
        
        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if usuario_autenticado:
            return template('app/views/html/tela_usuario', t=int(time()), usuario=dados_usuario.usuario, email=dados_usuario.email, saldo=dados_usuario.saldo, fatura=dados_usuario.fatura, investimentos=dados_usuario.investimentos)
        
        return redirect('/login')

    def cadastro(self):
        if request.method == 'GET':
            return template('app/views/html/cadastro', t=int(time()))
        if request.method == 'POST':
            usuario = request.forms.get('usuario')
            senha = request.forms.get('senha')
            email = request.forms.get('email')
            
            if self.model.adicionar_usuario(usuario, senha, email):
                redirect('/login')
            else:
                return template('app/views/html/cadastro', t=int(time()), erro="Erro ao cadastrar usuário")
        
    def deposito(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/deposito', t=int(time()))
        
        if request.method == 'POST':
            valor = float(request.forms.get('valor'))
            senha = request.forms.get('senha')
            
            if valor <= 0:
                return template('app/views/html/deposito', t=int(time()), erro="O valor deve ser maior que zero.")
                
            if self.model.depositar(valor, senha, dados_usuario.usuario):
                print(f"Depósito no valor de {valor} realizado com sucesso!")
                return redirect('/usuario') 
            return template('app/views/html/deposito', t=int(time()), erro="Erro ao realizar o depósito.")

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
                return template('app/views/html/transferencia', t=int(time()), erro="O valor deve ser maior que zero.")

            if self.model.transferencia(usuario_receptor, dados_usuario.usuario, valor, senha ):
                return redirect('/usuario')
            return template('app/views/html/transferencia', t=int(time()), erro="Erro ao realizar a transferencia.")

    def pagamentos(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login')

        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/pagamento', t=int(time()), saldo=dados_usuario.saldo)

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
                    return template('app/views/html/pagamento', t=int(time()), erro="O valor deve ser maior que zero.", saldo=dados_usuario.saldo)
                if self.model.pagamento_com_saldo(dados_usuario.usuario, senha, valor ):
                    print('pagamento realizado')
                    return redirect('/usuario')
                return template('app/views/html/pagamento', erro='Falha no pagamento',saldo=dados_usuario.saldo )

            return  template('app/views/html/pagamento', erro='Falha no pagamento',saldo=dados_usuario.saldo )
            


    def pagar_fatura(self):
        session_id = request.get_cookie('session_id')

        if not session_id:
            return redirect('/login'
        usuario_autenticado, dados_usuario = self.model.verificar_session_id(session_id)
        if not usuario_autenticado:
            return redirect('/login')

        if request.method == 'GET':
            return template('app/views/html/pagar-fatura', t=int(time()), fatura=dados_usuario.fatura,saldo=dados_usuario.saldo)


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
                    return template('app/views/html/pagamento', t=int(time()), erro="O valor deve ser maior que zero.", fatura=dados_usuario.fatura,saldo=dados_usuario.saldo)

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
        return template('app/views/html/cartao', t=int(time()), usuario=dados_usuario.usuario, fatura=dados_usuario.fatura)

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

        carteira = self.model.obter_carteira_usuario(dados_usuario.usuario) or {}

        # Obtém os preços das criptomoedas
        preco_btc, preco_eth, preco_doge = self.model.obter_precos()



        # Calcula o valor total que o usuário tem em cada moeda (quantidade * preço atual)
        valor_btc = carteira.get("BTC", 0) 
        valor_eth = carteira.get("ETH", 0) 
        valor_doge = carteira.get("DOGE", 0) 

        format_btc = f"{valor_btc:.8f}"
        format_eth = f"{valor_eth:.8f}"
        format_doge = f"{valor_doge:.8f}"

        # Emite uma mensagem com os preços e valores atualizados via WebSocket
        self.sio.emit('atualizar_dados', {
            'preco_btc': preco_btc,
            'preco_eth': preco_eth,
            'preco_doge': preco_doge,
            'valor_btc': float(f"{valor_btc:.8f}"),  
            'valor_eth': float(f"{valor_eth:.8f}"),
            'valor_doge': float(f"{valor_doge:.8f}"),
            'carteira': {moeda: float(f"{qtd:.8f}") for moeda, qtd in carteira.items()}  
        }, namespace='/investimentos')


        if request.method == 'GET':
            return template('app/views/html/investir', t=int(time()),
                investimentos=dados_usuario.investimentos, 
                usuario=dados_usuario.usuario, 
                saldo=dados_usuario.saldo,
                carteira=carteira,
                preco_btc=preco_btc,
                preco_eth=preco_eth,
                preco_doge=preco_doge,
                valor_btc=format_btc,
                valor_eth=format_eth,
                valor_doge=format_doge,
                dados_carteira_json=json.dumps(carteira)
            )

        if request.method == 'POST':
            data = request.json
            if not data:
                response.status = 400
                return {"erro": "Requisição inválida"}

            moeda = data.get("moeda")
            quantidade = data.get("quantidade")
            operacao = data.get("operacao")  # "comprar" ou "vender"

            # Validação da entrada
            if not moeda or quantidade is None or not operacao:
                response.status = 400
                return {"erro": "Dados incompletos"}

            try:
                quantidade = float(quantidade)
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                response.status = 400
                return {"erro": "Quantidade inválida"}

            # Determina se será uma compra ou venda
            if operacao == "comprar":
                sucesso = self.model.comprar_ativo(dados_usuario.usuario, moeda, quantidade)
            elif operacao == "vender":
                sucesso = self.model.vender_ativo(dados_usuario.usuario, moeda, quantidade)
            else:
                response.status = 400
                return {"erro": "Operação inválida"}

            if not sucesso:
                response.status = 400
                return {"erro": f"Falha ao {operacao} {moeda}"}

            # Atualiza a carteira do usuário após a operação
            carteira_atualizada = self.model.obter_carteira_usuario(dados_usuario.usuario)

            # Envia atualização para todos os clientes via WebSocket
            self.sio.emit('atualizar_carteira', {
                'carteira': carteira_atualizada
            }, namespace='/investimentos')

            response.status = 200
            return {"mensagem": f"{operacao.capitalize()} de {quantidade} {moeda} realizada com sucesso!"}

    