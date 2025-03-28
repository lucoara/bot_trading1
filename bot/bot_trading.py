# Importa as bibliotecas necessárias
from bitget.rest import RestClient
from binance.client import Client
import os
from dotenv import load_dotenv

# Carrega as credenciais do arquivo .env
load_dotenv()

BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET")
BITGET_PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Teste de conexão com a Bitget
try:
    print("🔄 Testando conexão com a Bitget...")
    bitget_client = RestClient(BITGET_API_KEY, BITGET_API_SECRET, BITGET_PASSPHRASE)
    server_time = bitget_client.common().get_system_time()
    print(f"✅ Conexão com Bitget OK! Server Time: {server_time['data']}")
except Exception as e:
    print(f"❌ Erro ao conectar na Bitget: {e}")

# Teste de conexão com a Binance
try:
    print("🔄 Testando conexão com a Binance...")
    binance_client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    server_time = binance_client.get_server_time()
    print(f"✅ Conexão com Binance OK! Server Time: {server_time['serverTime']}")
except Exception as e:
    print(f"❌ Erro ao conectar na Binance: {e}")
