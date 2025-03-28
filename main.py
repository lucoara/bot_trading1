import os
import pandas as pd
import numpy as np
import ta
import time
import ccxt
import asyncio
from dotenv import load_dotenv
from binance.client import Client
from telegram import Bot
from datetime import datetime

# Carregar variáveis do .env
load_dotenv()

# Configurar Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Conectar à Binance
try:
    binance_client = Client(os.getenv("BINANCE_API_KEY").strip(), os.getenv("BINANCE_SECRET_KEY").strip())
    print("✅ Conexão com Binance OK!")
except Exception as e:
    print(f"❌ Erro na conexão com a Binance: {e}")

# Conectar à Bitget via CCXT
try:
    bitget = ccxt.bitget({
        'apiKey': os.getenv("BITGET_API_KEY").strip(),
        'secret': os.getenv("BITGET_SECRET_KEY").strip(),
        'password': os.getenv("BITGET_PASS_PHRASE").strip(),
        'enableRateLimit': True
    })
    print("✅ Conexão com Bitget OK!")
except Exception as e:
    print(f"❌ Erro na conexão com a Bitget: {e}")

# Lista de ativos para monitorar
ativos = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'DOGE/USDT']

# Função para pegar dados do mercado na Binance
def get_binance_data(symbol, interval='5m'):
    klines = binance_client.get_klines(symbol=symbol.replace('/', ''), interval=interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_'])
    
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    
    # Adicionar Indicadores Técnicos
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ema9'] = ta.trend.EMAIndicator(df['close'], window=9).ema_indicator()
    df['ema21'] = ta.trend.EMAIndicator(df['close'], window=21).ema_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd()
    
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

# Verificar horário ideal de entrada
def horario_ideal():
    agora = datetime.now().hour
    return 9 <= agora <= 17

# Função assíncrona para enviar mensagem no Telegram
async def enviar_mensagem_telegram(mensagem):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem)

# Enviar sinal no Telegram
async def enviar_sinal_telegram(symbol):
    if horario_ideal():
        sinal = identificar_sinal(symbol)
        if sinal != "SEM SINAL":
            mensagem = f"📢 Sinal de {sinal} para {symbol}!"
            await enviar_mensagem_telegram(mensagem)

# Monitorar ativos a cada 5 minutos
async def monitorar_ativos():
    while True:
        for ativo in ativos:
            await enviar_sinal_telegram(ativo)
        await asyncio.sleep(300)  # Espera 5 minutos

# Testar conexões antes de rodar o bot
async def testar_conexoes():
    try:
        balance_binance = binance_client.get_account()
        print("✅ Conexão com Binance OK!")

        balance_bitget = bitget.fetch_balance()
        print("✅ Conexão com Bitget OK!")

        await enviar_mensagem_telegram("🤖 Bot de Trading iniciado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        await enviar_mensagem_telegram(f"❌ Erro na conexão: {e}")

# Iniciar monitoramento
if name == "__main__":
    asyncio.run(testar_conexoes())
    asyncio.run(monitorar_ativos())