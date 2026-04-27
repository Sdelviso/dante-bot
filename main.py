"""
@DanteAssitBot - Bot de Telegram para DANTE (Asistente Inmobiliario)
Integración con Claude API para procesamiento inteligente de mensajes de voz
"""

import os
import logging
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.error import TelegramError
import anthropic

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8443))
APP_URL = os.getenv('APP_URL')

# Inicializar cliente de Anthropic
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    welcome_message = """🏠 ¡Hola Sergio! Soy DANTE, tu asistente inmobiliario.

Puedo ayudarte con:
✓ Briefing diario
✓ Cualificación de leads
✓ Redacción de correos
✓ Asesoramiento comercial

Envíame un **mensaje de voz** o texto con lo que necesites.

Ejemplos:
🎤 "Hazme el briefing de hoy"
🎤 "Cualifica a este cliente que llamó..."
🎤 "Redacta un correo para..."

¿Qué necesitas hoy?"""

    await update.message.reply_text(welcome_message)
    logger.info(f"Usuario iniciado: {update.effective_user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    help_text = """📋 **Comandos DANTE:**

/start - Iniciar
/help - Esta ayuda
/status - Estado del bot

**Envía un mensaje de voz o texto con:**
• "briefing" - Resumen diario
• "califica" - Evaluar un lead
• "correo" - Redactar mensaje
• Tu pregunta/solicitud libre"""

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /status"""
    status_msg = f"""✅ **DANTE está operativo**

🔗 Bot: @DanteAssitBot
📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
🧠 Modelo: Claude 3.5 Sonnet
🎤 Entrada: Voz + Texto
📤 Salida: Respuestas inteligentes

Ready para procesar tu solicitud."""

    await update.message.reply_text(status_msg, parse_mode='Markdown')


async def transcribe_voice(file_path: str) -> str:
    """
    Transcribe audio a texto usando SpeechRecognition
    Fallback: Si el archivo es .oga de Telegram, lo convertimos
    """
    try:
        import speech_recognition as sr

        # Convertir .oga a .wav si es necesario
        if file_path.endswith('.oga'):
            logger.info(f"Convirtiendo {file_path} de .oga a .wav")
            wav_path = file_path.replace('.oga', '.wav')
            try:
                from pydub import AudioSegment
                sound = AudioSegment.from_ogg(file_path)
                sound.export(wav_path, format="wav")
                file_path = wav_path
            except Exception as e:
                logger.warning(f"No se pudo convertir OGA: {e}. Intentando directo...")

        # Transcribir
        recognizer = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language='es-ES')
        logger.info(f"Transcripción exitosa: {text}")
        return text

    except Exception as e:
        logger.error(f"Error en transcripción: {e}")
        return None


async def download_voice_file(context: ContextTypes.DEFAULT_TYPE, file_id: str) -> str:
    """Descargar archivo de voz de Telegram"""
    try:
        file = await context.bot.get_file(file_id)
        file_path = f"voice_{file_id}.oga"
        await file.download_to_drive(file_path)
        logger.info(f"Archivo descargado: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error descargando archivo: {e}")
        return None


async def process_with_claude(user_message: str, user_id: int) -> str:
    """
    Procesar mensaje con Claude usando el contexto DANTE
    """
    try:
        logger.info(f"Procesando con Claude: {user_message[:50]}...")

        # Construir contexto con información del usuario
        full_prompt = f"""Usuario (ID: {user_id}): {user_message}

---

Responde como DANTE. Sé directo, profesional y accionable."""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=DANTE_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        answer = response.content[0].text
        logger.info(f"Respuesta de Claude generada: {len(answer)} caracteres")
        return answer

    except Exception as e:
        logger.error(f"Error en Claude: {e}")
        return f"❌ Error procesando tu solicitud: {str(e)}"


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar mensajes de voz"""
    try:
        # Indicar que estamos procesando
        await update.message.chat.send_action("typing")

        user_id = update.effective_user.id
        logger.info(f"Mensaje de voz recibido de {user_id}")

        # Descargar archivo de voz
        voice = update.message.voice
        file_path = await download_voice_file(context, voice.file_id)

        if not file_path:
            await update.message.reply_text("❌ No pude descargar el archivo de voz. Intenta de nuevo.")
            return

        # Transcribir voz a texto
        await update.message.chat.send_action("typing")
        transcribed_text = await transcribe_voice(file_path)

        # Limpiar archivo descargado
        try:
            os.remove(file_path)
        except:
            pass

        if not transcribed_text:
            await update.message.reply_text("❌ No pude transcribir el audio. Asegúrate de hablar claro.")
            logger.warning(f"Transcripción fallida para {user_id}")
            return

        logger.info(f"Transcrito: {transcribed_text}")

        # Mostrar lo que se transcribió (opcional)
        await update.message.reply_text(f"🎤 Escuché: *{transcribed_text}*\n\nProcesando...", parse_mode='Markdown')

        # Procesar con Claude
        await update.message.chat.send_action("typing")
        response = await process_with_claude(transcribed_text, user_id)

        # Enviar respuesta
        await update.message.reply_text(response, parse_mode='Markdown')

    except TelegramError as e:
        logger.error(f"Error de Telegram: {e}")
        await update.message.reply_text(f"❌ Error de Telegram: {str(e)}")
    except Exception as e:
        logger.error(f"Error en handle_voice: {e}")
        await update.message.reply_text(f"❌ Error inesperado: {str(e)}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar mensajes de texto"""
    try:
        await update.message.chat.send_action("typing")

        user_id = update.effective_user.id
        text = update.message.text

        logger.info(f"Mensaje de texto de {user_id}: {text[:50]}...")

        # Procesar con Claude
        response = await process_with_claude(text, user_id)

        # Enviar respuesta
        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error en handle_text: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejar errores globales"""
    logger.error(f"Error en update {update}: {context.error}")


def main() -> None:
    """Iniciar el bot"""
    logger.info("Iniciando @DanteAssitBot...")

    # Verificar variables de entorno
    if not TELEGRAM_TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN no está configurado")
    if not CLAUDE_API_KEY:
        raise ValueError("❌ CLAUDE_API_KEY no está configurado")

    logger.info(f"Token de Telegram: {TELEGRAM_TOKEN[:20]}...")
    logger.info(f"API Key de Claude: {CLAUDE_API_KEY[:20]}...")

    # Crear aplicación
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))

    # Handlers de mensajes
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Handler de errores
    application.add_error_handler(error_handler)

    # Iniciar bot
    if WEBHOOK_URL and APP_URL:
        # Modo webhook (para producción)
        logger.info(f"Iniciando en modo webhook: {WEBHOOK_URL}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"{APP_URL}/{TELEGRAM_TOKEN}"
        )
    else:
        # Modo polling (para desarrollo)
        logger.info("Iniciando en modo polling (desarrollo)")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
