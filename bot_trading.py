import os
import pandas as pd
import numpy as np
import ta
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from binance.client import Client
from bitget.rest import RestClient
from telegram import Bot
import time

# Carregar variáveis do .env
load_dotenv()

# Configurar Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv 7880857109:AAG7Oe3fKo48MI9OgNSkYyJ2yt6g-w-oMAQ
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Conectar à Binance
binance_client = Client(os.getenv eDUxgm1zlFrbSVAVQ4vxhxezCcSw1BrzWdOqK0XsgQ1BepTHme1oGHM0rxy0Wfc4 , os.getenv ALAiEQnXw8LyEjRExPaO7dWMT9mJC0J61SOWqA6MPLdbh9SEe3HKTaXjBRm8YWnN

# Conectar à Bitget
bitget_client = RestClient(os.getenv bg_e97592c72c12a2b422fb3ec02ba4ae8e , os.getenv 22e22c52af06f1fb4bb1b9ef5d290527b709104f62fc5cbe73cc985b318c2408 , os.getenv lucoara86075260

# Lista de ativos para monitorar
ativos = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'BNBUSDT', 'SOLUSDT', 'DOTUSDT', 'MATICUSDT', 'AVAXUSDT', 'LTCUSDT', 'TRXUSDT', 'LINKUSDT', 'XLMUSDT', 'ATOMUSDT', 'ALGOUSDT', 'VETUSDT', 'ICPUSDT', 'FILUSDT', 'EGLDUSDT', 'MANAUSDT', 'SANDUSDT', 'AXSUSDT', 'AAVEUSDT', 'FTMUSDT']

# Função para pegar dados do mercado na Binance
def get_binance_data(symbol, interval='5m'):
    klines = binance_client.get_klines(symbol=symbol, interval=interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_'])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    
    # Adicionar Indicadores Técnicos
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ema9'] = ta.trend.EMAIndicator(df['close'], window=9).ema_indicator()
    df['ema21'] = ta.trend.EMAIndicator(df['close'], window=21).ema_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd()
    df['bollinger_high'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
    df['bollinger_low'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
    return df

# Função para identificar sinais de compra e venda
def identificar_sinal(symbol):
    df = get_binance_data(symbol)
    ultimo = df.iloc[-1]
    
    if ultimo['ema9'] > ultimo['ema21'] and ultimo['rsi'] > 50 and ultimo['macd'] > 0:
        return "COMPRA"
    elif ultimo['ema9'] < ultimo['ema21'] and ultimo['rsi'] < 50 and ultimo['macd'] < 0:
        return "VENDA"
    return "SEM SINAL"

# Função para verificar horário ideal de entrada
def horario_ideal():
    agora = datetime.now().hour
    return 9 <= agora <= 17  # Exemplo: operar das 24h

# Enviar sinal no Telegram
def enviar_sinal_telegram(symbol):
    if horario_ideal():
        sinal = identificar_sinal(symbol)
        if sinal != "SEM SINAL":
            mensagem = f"📢 Sinal de {sinal} para {symbol}!"
            bot.send_message(chat_id='SEU_CHAT_ID', text=mensagem)

# Loop para enviar sinais a cada 5 minutos
def monitorar_ativos():
    while True:
        for ativo in ativos:
            enviar_sinal_telegram(ativo)
        time.sleep(300)  # Espera 5 minutos
import os
from dotenv import load_dotenv
from bitget.rest import RestClient
import ccxt

# Carregar variáveis do .env
load_dotenv()

# Configurar a API da Bitget
BITGET_API_KEY = os.getenv("BITGET_API_KEY")
BITGET_SECRET_KEY = os.getenv("BITGET_SECRET_KEY")

client = RestClient(BITGET_API_KEY, BITGET_SECRET_KEY, "passphrase")

# Testar conexão Bitget
try:
    server_time = client.common_get_system_time()
    print(f"Conexão com Bitget OK! Server Time: {server_time}")
except Exception as e:
    print(f"Erro na conexão com a Bitget: {e}")

# Configurar a API da Binance
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET_KEY,
    'options': {'defaultType': 'spot'}
})

# Testar conexão Binance
try:
    balance = exchange.fetch_balance()
    print("Conexão com Binance OK!")
except Exception as e:
    print(f"Erro na conexão com a Binance: {e}")

# Iniciar monitoramento
monitorar_ativos()
