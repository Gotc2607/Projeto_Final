import sqlite3
import bcrypt
import os

class Banco:

    def __init__(self,):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir= os.path.join(base_dir, 'db')
        database_path = os.path.join(db_dir, 'Usuario.db')

        self.conexao = sqlite3.connect(database_path)
        self.cursor = self.conexao.cursor()
    


    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            email TEXT NOT NULL,
            saldo REAL DEFAULT 0,
            fatura REAL DEFAULT 0
        );
        ''')
        self.conexao.commit()

    def adicionar_usuario(self, usuario, senha_hash, email):

        self.cursor.execute("INSERT INTO Usuario (usuario, senha, email) VALUES (?, ?, ?)", (usuario, senha_hash, email))
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
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)

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
    
    def depositar(self, usuario, valor):
        """
        Deposita um valor na conta do usuário.
        """
        saldo = self.obter_saldo(usuario)
        saldo += valor
        self.cursor.execute("UPDATE Usuario SET saldo = ? WHERE usuario = ?", (saldo, usuario))
        self.conexao.commit()
        return saldo

    def sacar(self, usuario, valor):    
        """
        Saca um valor da conta do usuário.
        """
        saldo = self.obter_saldo(usuario)
        saldo -= valor
        self.cursor.execute("UPDATE Usuario SET saldo = ? WHERE usuario = ?", (saldo, usuario))
        self.conexao.commit()
        return saldo