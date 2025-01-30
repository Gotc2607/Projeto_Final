import sqlite3
import bcrypt
import os
import uuid


class Banco:

    def __init__(self,):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir= os.path.join(base_dir, 'db')
        database_path = os.path.join(db_dir, 'Usuario.db')

        self.conexao = sqlite3.connect(database_path)
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
            tipo TEXT CHECK(tipo IN ('deposito', 'saque')),
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
    
    def registrar_deposito(self, usuario_id, valor):
        self.cursor.execute("INSERT INTO transacoes (usuario_id, tipo, valor) VALUES (?,'deposito', ?)", 
                            (usuario_id, valor))
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
        