import sqlite3
from app.controllers.datbase import Banco

class Ws_Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def criar_carteira(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS carteira (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                moeda TEXT NOT NULL,
                quantidade REAL NOT NULL
            )
        """)
        self.conn.commit()

    def get_user_portfolio(self, usuario):
        self.cursor.execute("SELECT moeda, quantidade FROM carteira WHERE usuario = ?", (usuario,))
        return dict(self.cursor.fetchall())

    def update_portfolio(self, usuario, moeda, quantidade):
        carteira = self.get_user_portfolio(usuario)
        if moeda in carteira:
            nova_quantidade = carteira[moeda] + quantidade
            if nova_quantidade <= 0:
                self.cursor.execute("DELETE FROM carteira WHERE usuario = ? AND moeda = ?", (usuario, moeda))
            else:
                self.cursor.execute("UPDATE carteira SET quantidade = ? WHERE usuario = ? AND moeda = ?", (nova_quantidade, usuario, moeda))
        else:
            if quantidade > 0:
                self.cursor.execute("INSERT INTO carteira (usuario, moeda, quantidade) VALUES (?, ?, ?)", (usuario, moeda, quantidade))
        self.conn.commit()
