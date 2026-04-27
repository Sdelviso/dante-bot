"""
Script para testear el bot localmente sin Telegram
Valida que las APIs estén funcionando antes de deployar
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

print("=" * 60)
print("🧪 TEST LOCAL - @DanteAssitBot")
print("=" * 60)

# Test 1: Variables de entorno
print("\n[1/4] Verificando variables de entorno...")
try:
    assert TELEGRAM_TOKEN, "❌ TELEGRAM_TOKEN no configurado"
    assert CLAUDE_API_KEY, "❌ CLAUDE_API_KEY no configurado"
    print(f"✅ TELEGRAM_TOKEN: {TELEGRAM_TOKEN[:20]}...")
    print(f"✅ CLAUDE_API_KEY: {CLAUDE_API_KEY[:20]}...")
except AssertionError as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Conexión a Claude
print("\n[2/4] Probando conexión a Claude API...")
try:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[{"role": "user", "content": "Di 'Hola DANTE'"}]
    )
    print(f"✅ Claude API funcionando")
    print(f"   Respuesta: {response.content[0].text[:50]}...")
except Exception as e:
    print(f"❌ Error con Claude: {e}")
    exit(1)

# Test 3: Contexto DANTE
print("\n[3/4] Testando contexto DANTE...")
try:
    DANTE_PROMPT = """Eres DANTE, asistente inmobiliario. Responde brevemente."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        system=DANTE_PROMPT,
        messages=[{"role": "user", "content": "¿Cómo está el mercado inmobiliario hoy?"}]
    )
    print(f"✅ DANTE respondiendo correctamente")
    print(f"   Respuesta DANTE: {response.content[0].text[:80]}...")
except Exception as e:
    print(f"❌ Error en contexto DANTE: {e}")
    exit(1)

# Test 4: Telegram Bot Info
print("\n[4/4] Verificando Bot de Telegram...")
try:
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data.get('ok'):
        bot_info = data['result']
        print(f"✅ Bot verificado: @{bot_info['username']}")
        print(f"   ID: {bot_info['id']}")
        print(f"   Nombre: {bot_info['first_name']}")
    else:
        print(f"❌ Token inválido o expirado")
        exit(1)
except Exception as e:
    print(f"❌ Error Telegram: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS PASARON")
print("=" * 60)
print("\nEl bot está listo para:")
print("  1. Ejecutar localmente: python main.py")
print("  2. Desplegar en Railway (DEPLOYMENT_RAILWAY.md)")
print("\n¡A producción! 🚀")
