"""
Script para configurar el webhook de Telegram
Ejecuta esto después de deployar en Railway/Render
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
APP_URL = os.getenv('APP_URL')

if not TELEGRAM_TOKEN or not APP_URL:
    print("❌ Error: TELEGRAM_TOKEN o APP_URL no están configurados")
    print("Edita tu archivo .env y vuelve a intentar")
    exit(1)

# URL del webhook
webhook_url = f"{APP_URL}/{TELEGRAM_TOKEN}"

print(f"🔗 Configurando webhook...")
print(f"   Token: {TELEGRAM_TOKEN[:20]}...")
print(f"   URL: {webhook_url}")

# Llamar a la API de Telegram
response = requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
    json={"url": webhook_url}
)

if response.status_code == 200:
    data = response.json()
    if data.get('ok'):
        print("✅ Webhook configurado correctamente!")
        print(f"   Respuesta: {data.get('description')}")

        # Verificar
        verify = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
        ).json()

        if verify.get('ok'):
            info = verify.get('result', {})
            print(f"\n📊 Estado del webhook:")
            print(f"   URL: {info.get('url')}")
            print(f"   Pendientes: {info.get('pending_update_count')}")
            print(f"   IP permitida: {info.get('ip_address')}")
    else:
        print(f"❌ Error: {data.get('description')}")
else:
    print(f"❌ Error HTTP: {response.status_code}")
    print(response.text)
