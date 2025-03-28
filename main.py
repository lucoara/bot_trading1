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
TELEGRAM_BOT_TOKEN = os.getenv7880857109:AAG7Oe3fKo48MI9OgNSkYyJ2yt6g-w-oMAQ
TELEGRAM_CHAT_ID = os.getenv7268477518
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Conectar à Binance
try:
    binance_client = Client(os.getenv eDUxgm1zlFrbSVAVQ4vxhxezCcSw1BrzWdOqK0XsgQ1BepTHme1oGHM0rxy0Wfc4.strip(), os.getenv ALAiEQnXw8LyEjRExPaO7dWMT9mJC0J61SOWqA6MPLdbh9SEe3HKTaXjBRm8YWnN.strip())
    print("✅ Conexão com Binance OK!")
except Exception as e:
    print(f"❌ Erro na conexão com a Binance: {e}")

# Conectar à Bitget via CCXT
try:
    bitget = ccxt.bitget({
        'apiKey': os.getenv bg_e97592c72c12a2b422fb3ec02ba4ae8e .strip(),
        'secret': os.getenv 22e22c52af06f1fb4bb1b9ef5d290527b709104f62fc5cbe73cc985b318c2408.strip (),
        'password': os.getenv lucoara86075260 .strip(),
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
if __name__ == "__main__":
    asyncio.run(testar_conexoes())
    asyncio.run(monitorar_ativos())
