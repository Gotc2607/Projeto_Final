import sqlite3
import bcrypt
import os
import uuid

class Banco:

    def __init__(self,):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir= os.path.join(base_dir, 'db')
        database_path = os.path.join(db_dir, 'Usuario.db')

        self.conexao = sqlite3.connect(database_path, check_same_thread=False)
        self.cursor = self.conexao.cursor()
    


    def criar_tabela1(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            email TEXT NOT NULL,
            saldo REAL DEFAULT 0,
            fatura REAL DEFAULT 0,
            investimentos REAL DEFAULT 0
        );
        ''')
        self.conexao.commit()
    
    def cria_tabela_depositos(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN ('deposito', 'transferencia', 'pagamento')),
            valor REAL,
            data TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        ''')
        self.conexao.commit()

    def obter_depositos(self, usuario_id):
        self.cursor.execute(
            "SELECT valor, data FROM transacoes WHERE usuario_id = ? AND tipo = 'deposito' ORDER BY data DESC",
            (usuario_id,)
        )
        depositos =self.cursor.fetchall()
        print(depositos)
        if depositos:
            return depositos
        else:
            return [] 
    
    def obter_transferencias(self, usuario_id):
        self.cursor.execute(
            "SELECT valor, data FROM transacoes WHERE usuario_id = ? AND tipo = 'transferencia' ORDER BY data DESC",
            (usuario_id,)
        )
        transferencias =self.cursor.fetchall()
        print(transferencias)
        if transferencias:
            return transferencias
        else:
            return [] 
    
    def obter_pagamentos(self, usuario_id):
        self.cursor.execute(
            "SELECT valor, data FROM transacoes WHERE usuario_id = ? AND tipo = 'pagamento'  ORDER BY data DESC",
            (usuario_id,)
        )
        pagamentos =self.cursor.fetchall()
        if pagamentos:
            return pagamentos
        else:
            return [] 

    
    def registrar_operacoes(self, usuario_id, tipo,valor):
        self.cursor.execute("INSERT INTO transacoes (usuario_id, tipo, valor) VALUES (?, ?, ?)", 
                            (usuario_id, tipo ,valor))
        self.conexao.commit()

    def adicionar_usuario(self, session_id, usuario, senha_hash, email):

        self.cursor.execute("INSERT INTO Usuario (session_id, usuario, senha, email) VALUES (?, ?, ?, ?)", (session_id, usuario, senha_hash, email))
        print('usuario adicionado')
        self.conexao.commit()


    def hash_senha(self, senha):
        """
        Hashea a senha utilizando bcrypt.
        """
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    def verificar_senha(self, senha, senha_hash):
        """
        Verifica se a senha corresponde ao hash.
        """
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            return True
        return False

    def verificar_usuario(self, usuario):
        self.cursor.execute("SELECT 1 FROM Usuario WHERE usuario = ?", (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            return True
        return False

    def obter_dados_usuario(self, usuario):
        """
        Retorna os dados do usuário a partir do username.
        """
        self.cursor.execute("SELECT * FROM Usuario WHERE usuario = ?", (usuario,))
        print('dados do usuario obtidos')
        return self.cursor.fetchone() #[]


    def obter_saldo(self, usuario):
        """
        Retorna o saldo do usuário.
        """
        self.cursor.execute("SELECT saldo FROM Usuario WHERE usuario = ?", (usuario,))
        return self.cursor.fetchone()[0]

    def obter_fatura(self, usuario):
        """
        Retorna a fatura do usuário.
        """
        self.cursor.execute("SELECT fatura FROM Usuario WHERE usuario = ?", (usuario,))
        return self.cursor.fetchone()[0]

    
    def deposito(self, saldo, usuario):
        self.cursor.execute("UPDATE Usuario SET saldo = ? WHERE usuario = ?", (saldo, usuario))
        self.conexao.commit()
        return True

    def gerar_session_id(self, usuario):
        """
        Gera um session_id único para o usuário.
        """
        session_id = str(uuid.uuid4())
        self.cursor.execute("UPDATE Usuario SET session_id = ? WHERE usuario = ?", (session_id, usuario))
        self.conexao.commit()
        return session_id

    def verificar_session_id(self, session_id):
        """
        Verifica se o session_id é válido e retorna os dados do usuário associado.
        """
        self.cursor.execute("SELECT * FROM Usuario WHERE session_id = ?", (session_id,))
        usuario = self.cursor.fetchone()
        return usuario  # Retorna None se o session_id for inválido

    def obter_usuario_por_session_id(self, session_id):
        """
        Retorna os dados do usuário a partir do session_id.
        """
        self.cursor.execute("SELECT usuario FROM Usuario WHERE session_id = ?", (session_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def transferencia(self,usuario_receptor, usuario_atual,valor,  senha):
        #tira do usuario que está mandando 
        if self.cursor.execute("UPDATE Usuario SET saldo = saldo - ? WHERE usuario = ?", (valor, usuario_atual))and  self.cursor.execute("UPDATE Usuario SET saldo = saldo + ? WHERE usuario = ?", (valor, usuario_receptor)):

            print(f'transferencia de {usuario_atual} para {usuario_receptor} concluida')
        
            self.conexao.commit()
            return True
        return False

    def pagamento_com_saldo(self, usuario,valor):
        if self.cursor.execute("UPDATE Usuario SET saldo = saldo - ? WHERE usuario = ?", (valor, usuario)):
            self.conexao.commit()
            return True
        return False

    def pagamento_com_cartao(self,usuario, valor):
        if self.cursor.execute("UPDATE Usuario SET fatura = fatura + ? WHERE usuario = ?", (valor, usuario)):
            self.conexao.commit()
            return True
        return False

    def pagar_fatura(self, usuario, valor):
        if self.cursor.execute("UPDATE Usuario SET fatura = fatura - ? WHERE usuario = ?", (valor, usuario)):
            self.conexao.commit()
            return True
        return False
#--------------------------------------------------------------------------
    def criar_carteira(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS carteira (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                saldo_disponivel REAL DEFAULT 0,
                moeda TEXT NOT NULL,
                quantidade REAL DEFAULT 0,
                UNIQUE(usuario, moeda)
            )
        """)
        self.conexao.commit()

    def obter_saldo_disponivel(self, usuario):
        self.cursor.execute("SELECT saldo_disponivel FROM carteira WHERE usuario = ?", (usuario,))
        return self.cursor.fetchone()[0]

    def deposito_saldo_disponivel(self, usuario, quantidade):
        if self.cursor.execute(""" UPDATE carteira SET saldo_disponivel = saldo_disponivel + ? WHERE usuario = ?""", (quantidade, usuario)):
            self.conexao.commit()
            return True
        return False

    def compra_saldo_disponivel(self, usuario, quantidade):
        if self.cursor.execute(""" UPDATE carteira SET saldo_disponivel = saldo_disponivel - ? WHERE usuario = ?""", (quantidade, usuario)):
            self.conexao.commit()
            return True
        return False


    def adicionar_carteira_usuario(self, usuario, moeda, quantidade):
        self.cursor.execute("""INSERT INTO carteira (usuario, moeda, quantidade) VALUES (?,?,?)""",(usuario,moeda, quantidade))
        self.conexao.commit()
    
    def criar_carteira_usuario(self, usuario):
    # Cria automaticamente uma carteira para o usuário se ele ainda não tiver uma.
    
        self.cursor.execute("SELECT COUNT(*) FROM carteira WHERE usuario = ?", (usuario,))
        existe = self.cursor.fetchone()[0]

        if not existe:
        # Moedas disponíveis no sistema
            moedas = ["BTC", "ETH", "DOGE"]
            for moeda in moedas:
                self.cursor.execute("INSERT INTO carteira (usuario, moeda, quantidade) VALUES (?, ?, ?)", (usuario, moeda, 0))
        
            self.conexao.commit()
            print(f"Carteira criada para o usuário {usuario}")

    def Obter_carteira_usuario(self, usuario):
        self.cursor.execute("SELECT moeda, quantidade FROM carteira WHERE usuario = ?", (usuario,))
        resultado = self.cursor.fetchall()
        carteira = {moeda: quantidade for moeda, quantidade in resultado}
        
        return dict(resultado) if resultado else {}

    def atualizar_carteira(self, usuario, moeda, quantidade):
        carteira = self.Obter_carteira_usuario(usuario)
        if moeda in carteira:
            nova_quantidade = carteira[moeda] + quantidade
            if nova_quantidade <= 0:
                self.cursor.execute("DELETE FROM carteira WHERE usuario = ? AND moeda = ?", (usuario, moeda))
                return 
            else:
                self.cursor.execute("UPDATE carteira SET quantidade = ? WHERE usuario = ? AND moeda = ?", (nova_quantidade, usuario, moeda))
        else:
            if quantidade > 0:
                self.cursor.execute("INSERT INTO carteira (usuario, moeda, quantidade) VALUES (?, ?, ?)", (usuario, moeda, quantidade))

        
        self.conexao.commit()
        return True

    def listar_usuarios(self):
        """Retorna uma lista com todos os usuários e suas carteiras no banco de dados."""
        query = """
            SELECT u.id, u.usuario, u.email, u.saldo, c.moeda, c.quantidade
            FROM Usuario u
            LEFT JOIN carteira c ON u.usuario = c.usuario
        """
        self.cursor.execute(query)
        usuarios = self.cursor.fetchall()
        return usuarios