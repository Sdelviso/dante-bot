#!/usr/bin/env python3
"""
DANTE Bot - Asistente inmobiliario por Telegram
Versión simplificada sin conflictos de dependencias
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Validar variables
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN no está configurado")
if not CLAUDE_API_KEY:
    raise ValueError("❌ CLAUDE_API_KEY no está configurado")

logger.info(f"✅ Token Telegram: {TELEGRAM_TOKEN[:10]}...")
logger.info(f"✅ Claude API Key: {CLAUDE_API_KEY[:10]}...")

# Inicializar cliente de Anthropic
try:
    client = Anthropic(api_key=CLAUDE_API_KEY)
    logger.info("✅ Cliente Anthropic inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error al inicializar Anthropic: {e}")
    raise

# Almacenar conversaciones por usuario
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user_id = update.effective_user.id
    conversations[user_id] = []

    message = """🤖 **DANTE - Asistente Inmobiliario**

Hola, soy DANTE, tu asistente de IA para gestión inmobiliaria.

Puedo ayudarte con:
✅ Briefing diario
✅ Cualificación de leads
✅ Redacción de correos
✅ Análisis de mercado

Envíame un mensaje de voz o texto y responderé. 🎤📝"""

    await update.message.reply_text(message, parse_mode='Markdown')
    logger.info(f"Usuario {user_id} inició conversación")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar mensajes de usuario"""
    user_id = update.effective_user.id

    # Obtener texto del mensaje
    text = update.message.text
    if not text:
        await update.message.reply_text("⚠️ No entendí tu mensaje. Intenta de nuevo.")
        return

    logger.info(f"[Usuario {user_id}]: {text}")

    # Inicializar conversación del usuario si no existe
    if user_id not in conversations:
        conversations[user_id] = []

    # Añadir mensaje del usuario al historial
    conversations[user_id].append({
        "role": "user",
        "content": text
    })

    # Contexto DANTE
    system_prompt = """Eres DANTE, un asistente experto en inmobiliaria.
Tienes más de 23 años de experiencia en el sector.
Respondes de forma concisa, profesional y directa.
Enfócate en soluciones prácticas para agentes inmobiliarios."""

    try:
        # Llamar a Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=conversations[user_id]
        )

        # Extraer respuesta
        assistant_message = response.content[0].text

        # Añadir respuesta al historial
        conversations[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        # Limitar historial a últimos 20 mensajes
        if len(conversations[user_id]) > 40:
            conversations[user_id] = conversations[user_id][-40:]

        logger.info(f"[DANTE responde]: {assistant_message[:50]}...")

        # Enviar respuesta
        await update.message.reply_text(assistant_message, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"❌ Error al procesar mensaje: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
📚 **Comandos disponibles:**
/start - Reiniciar conversación
/help - Mostrar esta ayuda
/clear - Limpiar historial

Simplemente envía un mensaje y DANTE responderá. 🤖
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /clear - limpiar historial"""
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text("🧹 Historial limpiado. Nueva conversación iniciada.")
    logger.info(f"Usuario {user_id} limpió el historial")

def main():
    """Iniciar el bot"""
    logger.info("🚀 Iniciando DANTE Bot...")

    # Crear aplicación
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Registrar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot iniciado. Esperando mensajes...")

    # Iniciar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
