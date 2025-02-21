import time
import random
from time import sleep
from app.models.user_account import UsuarioModel

class preco:

    def __init__(self,sio):
        self.crypto_prices = {"BTC": 567.047, "ETH": 15.490, "DOGE": 1.48}
        self.sio = sio
        self.model = UsuarioModel()

    def atualizar_precos_periodicamente(self):
        """Simula a flutuação dos preços e atualiza via WebSocket a cada 5 segundos."""
        while True:
            # Simula a variação dos preços (exemplo: +/- 2%)
            fator_btc = random.uniform(0.98, 1.02)
            fator_eth = random.uniform(0.98, 1.02)
            fator_doge = random.uniform(0.98, 1.02)


            # Obtém os novos preços após a atualização
            preco_btc, preco_eth, preco_doge = self.model.obter_precos()

            preco_btc = preco_btc * fator_btc
            preco_eth = preco_eth * fator_eth
            preco_doge = preco_doge * fator_doge

            time.sleep(2)  # Atualiza a cada 2 segundos