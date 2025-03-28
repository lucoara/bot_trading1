import ccxt
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Obter credenciais da Bitget
bitget_api_key = os.getenv("BITGET_API_KEY")
bitget_secret_key = os.getenv("BITGET_SECRET_KEY")
bitget_passphrase = os.getenv("BITGET_PASSPHRASE")

try:
    # Criar conexão com a Bitget via CCXT
    exchange = ccxt.bitget({
        'apiKey': bitget_api_key,
        'secret': bitget_secret_key,
        'password': bitget_passphrase,
        'options': {'defaultType': 'swap'}  # Define o tipo de mercado (swap = futuros)
    })

    # Buscar saldo da conta
    balance = exchange.fetch_balance()
    print("✅ Conexão com a Bitget bem-sucedida! Saldo disponível:", balance)

except Exception as e:
    print(f"❌ Erro ao conectar na Bitget: {e}")
