import sqlite3
import bcrypt

class banco_de_dados:

    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.cursor = self.con.cursor()

    def Criar_tabela(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            saldo REAl DEFAULT 0
        );
        ''')
       
        #verificar se a senha e o nome de usuario então certos
    def verificar_usuario(self, usuario, senha):
        self.cursor.execute("SELECT senha FROM banco_de_dados WHERE usuario = ?", (usuario,))
        resultado = self.cursor.fetchone()
       
        if resultado and bcrypt.checkpw(senha.encode(), resultado[0]):
            return True
        else:
            return False

    def adicionar_usuario(self, usuario, senha):
        """Adiciona um novo usuário com senha criptografada."""
        if self.verificar_nome_usuario(usuario):
            return "Usuário já existe."
        
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())#cria asenha criptografada
        self.cursor.execute('INSERT INTO banco_de_dados (usuario, senha) VALUES (?, ?)', (usuario, senha_hash))
        self.con.commit()
        return "Usuário adicionado com sucesso."

    

    def ver_saldo(self, senha):
        self.cursor.execute('SELECT saldo FROM banco_de_dados WHERE senha = ?', (senha,))
        resultado = self.cursor.fetchone()

        if resultado is not None:
            saldo = resultado[0]
            return saldo
        else:
            return None


    def salvar(self):

       if self.con:
        self.con.commit()