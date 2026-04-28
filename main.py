#!/usr/bin/env python3
"""
DANTE Bot - Asistente inmobiliario por Telegram
Versión con Groq (100% gratis)
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validar variables
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN no está configurado")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY no está configurado")

logger.info(f"✅ Token Telegram: {TELEGRAM_TOKEN[:10]}...")
logger.info(f"✅ Groq API Key: {GROQ_API_KEY[:10]}...")

# Inicializar cliente de Groq
try:
    client = Groq(api_key=GROQ_API_KEY)
    logger.info("✅ Cliente Groq inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error al inicializar Groq: {e}")
    raise

# Almacenar conversaciones por usuario
conversations = {}

# Contexto DANTE
DANTE_SYSTEM_PROMPT = """Eres DANTE, el asistente inmobiliario virtual de Sergio Delviso, responsable comercial de una oficina inmobiliaria en Aincat con 23 años de experiencia en el sector.

Tu tono es profesional, directo y confiable. Hablas en español con un registro corporativo pero accesible.

Tienes estas capacidades clave:
1. BRIEFING DIARIO: Resumir agenda, tareas, correos urgentes, leads, clima y mercado
2. CUALIFICACIÓN DE LEADS: Evaluar calidad de demandantes y vendedores, asignar prioridad
3. REDACCIÓN DE CORREOS: Crear correos profesionales para clientes inmobiliarios
4. ASESORAMIENTO: Orientar en precios, negociación, tácticas de cierre

Cuando recibas un mensaje de voz transcrito de Sergio:
- Identifica la intención (¿briefing?, ¿valorar un lead?, ¿redactar correo?)
- Responde de forma concisa y accionable
- Si necesitas más contexto, pregunta específicamente
- Siempre ofrece próximos pasos claros

Firma tus respuestas como "DANTE" al final."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    conversations[user_id] = []

    # LOG: Capturar chat_id
    logger.info(f"📞 CHAT_ID={chat_id} (Usuario: {user_id}) — /start recibido")

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
    chat_id = update.effective_chat.id

    # Obtener texto del mensaje
    text = update.message.text
    if not text:
        await update.message.reply_text("⚠️ No entendí tu mensaje. Intenta de nuevo.")
        return

    # LOG IMPORTANTE: Imprimir chat_id para configuración Telegram
    logger.info(f"📞 CHAT_ID={chat_id}")
    logger.info(f"[Usuario {user_id}]: {text}")

    # Inicializar conversación del usuario si no existe
    if user_id not in conversations:
        conversations[user_id] = []

    # Añadir mensaje del usuario al historial
    conversations[user_id].append({
        "role": "user",
        "content": text
    })

    try:
        # Preparar mensajes con system al inicio (formato correcto para Groq)
        messages = [
            {"role": "system", "content": DANTE_SYSTEM_PROMPT},
            *conversations[user_id]
        ]

        # Llamar a Groq con modelo actual disponible
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )

        # Extraer respuesta
        assistant_message = response.choices[0].message.content

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
    logger.info("🚀 Iniciando DANTE Bot (Groq)...")

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
