# 🏠 @DanteAssitBot - Asistente Inmobiliario en Telegram

Bot de Telegram alimentado por Claude API que asiste a Sergio Delviso en operaciones inmobiliarias.

**Estado:** ✅ Listo para producción

---

## 📋 Características

- ✅ **Entrada de voz**: Envía mensajes de voz, el bot transcribe automáticamente
- ✅ **Procesamiento inteligente**: Claude 3.5 Sonnet con contexto DANTE
- ✅ **Skills operativos**:
  - Briefing diario (agenda, tareas, leads, mercado)
  - Cualificación de leads (demandantes y vendedores)
  - Redacción de correos profesionales
  - Asesoramiento comercial (precios, negociación)
- ✅ **Respuestas en Markdown** formateadas para lectura fácil
- ✅ **Bajo latencia**: Procesamiento rápido incluso con archivos de voz grandes

---

## 🔧 Requisitos Previos

### Antes de empezar, necesitas:

1. **Bot de Telegram registrado** en @BotFather
   - Ya tienes: `@DanteAssitBot`
   - Ya tienes el TELEGRAM_TOKEN

2. **Cuenta de Anthropic** con acceso a Claude API
   - API Key disponible en: https://console.anthropic.com/

3. **Python 3.10+** (en tu computadora para pruebas locales)

4. **Servicio de hosting** (Railway, Render, Heroku, etc.)

---

## 🚀 Instalación Local (Desarrollo)

### Paso 1: Clonar o descargar los archivos

```bash
# Crear carpeta del proyecto
mkdir dante-bot
cd dante-bot

# Copiar los archivos:
# - main.py
# - requirements.txt
# - .env.example
```

### Paso 2: Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota sobre pydub**: Si usas macOS/Linux, también necesitas `ffmpeg`:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Descargar desde: https://ffmpeg.org/download.html
```

### Paso 4: Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores:
# TELEGRAM_TOKEN=Tu_Token_De_BotFather
# CLAUDE_API_KEY=sk-ant-Tu_API_Key
```

### Paso 5: Ejecutar localmente

```bash
python main.py
```

Deberías ver:
```
INFO:__main__:Iniciando @DanteAssitBot...
INFO:__main__:Iniciando en modo polling (desarrollo)
```

---

## 📱 Usar el Bot (Localmente)

1. Abre Telegram y busca **@DanteAssitBot**
2. Envía `/start` para iniciar
3. Prueba estos comandos:
   - `/help` - Ver ayuda
   - `/status` - Estado del bot
   - Envía un **mensaje de voz** con lo que necesites:
     - "Dame el briefing de hoy"
     - "Cualifica a este cliente que llamó..."
     - "Redacta un correo para un vendedor"
   - O envía **texto** directamente

### Ejemplos de Entrada:

**Voz transcrita:** "Hazme el briefing de hoy con la agenda, correos y clima"
**Respuesta DANTE:**
```
📋 BRIEFING DIARIO - 27 de abril

⏰ Agenda:
- Llamada con cliente Castelldefels 11:00h
- Visita a propiedad Cornell 14:30h

📧 Correos urgentes: 2 nuevos
- Lead cualificado (presupuesto 350k)

🌡️ Clima: 22°C, parcialmente nublado

💡 Recomendación: Priorizar contacto con lead de 350k
(Buena solvencia, tiempo ajustado)

DANTE
```

---

## 🌐 Deployment a Producción

Elige una opción (Railway es la más sencilla):

### Opción 1: Railway ⭐ (RECOMENDADO)

**Ventaja**: Gratuita para empezar, muy fácil.

#### 1.1 - Preparar el repositorio

Crea un archivo `Procfile` en la raíz del proyecto:
```
web: python main.py
```

Crea un repositorio en GitHub:
```bash
git init
git add .
git commit -m "Initial commit: DANTE Bot"
git remote add origin https://github.com/TU_USER/dante-bot.git
git push -u origin main
```

#### 1.2 - Deploy en Railway

1. Ve a https://railway.app
2. Haz login con GitHub
3. Haz clic en **"New Project"** → **"Deploy from GitHub"**
4. Selecciona tu repositorio `dante-bot`
5. Railway detectará que es Python automáticamente

#### 1.3 - Configurar Variables de Entorno en Railway

En el Dashboard de Railway:
1. Haz clic en tu proyecto
2. Pestaña **"Variables"**
3. Añade:
   - `TELEGRAM_TOKEN` = Tu token de @BotFather
   - `CLAUDE_API_KEY` = Tu API Key de Anthropic
   - `WEBHOOK_URL` = (Railway generará automáticamente la URL)
   - `APP_URL` = Tu URL de Railway (ej: `https://dante-bot-prod.railway.app`)

#### 1.4 - Railway generará la URL automáticamente

Copiar la URL de tu servidor Railway (ej: `https://dante-bot-prod.railway.app`)

---

### Opción 2: Render

1. Ve a https://render.com
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio GitHub
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python main.py`
6. Añade las variables de entorno (igual que Railway)
7. Deploy

---

### Opción 3: Heroku (Aunque está pagando ahora)

1. Ve a https://dashboard.heroku.com
2. **New** → **Create New App**
3. Conecta GitHub
4. Enable "Automatic Deploys"
5. En **Settings**, añade las variables de entorno
6. Deploy

---

## 🔌 Configurar Webhook de Telegram

Una vez que tu bot esté en producción, necesitas registrar el webhook:

```bash
# En tu terminal (con cURL):
curl -X POST https://api.telegram.org/botTU_TOKEN/setWebhook \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://tu-dominio.railway.app/TU_TOKEN"}'

# O usando Python:
import requests
requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
    json={"url": f"{APP_URL}/{TELEGRAM_TOKEN}"}
)
```

Verificar que funcionó:
```bash
curl https://api.telegram.org/botTU_TOKEN/getWebhookInfo
```

---

## 📊 Monitoreo

### En Railway:
- Pestaña **"Logs"** para ver logs en tiempo real
- Pestaña **"Metrics"** para ver CPU/memoria

### En Render:
- Pestaña **"Logs"** similar

### Troubleshooting:

Si el bot no responde:
1. Revisa los logs (busca errores de API)
2. Verifica variables de entorno: `echo $TELEGRAM_TOKEN`
3. Testea localmente primero: `python main.py`

---

## 🧪 Testing Completo

### Test Local:

```bash
# Terminal 1: Ejecutar bot
python main.py

# Terminal 2: Testear API (opcional)
python -c "
import requests
token = 'YOUR_TOKEN'
url = f'https://api.telegram.org/bot{token}/getMe'
print(requests.get(url).json())
"
```

### Test en Producción:

1. Abre Telegram → @DanteAssitBot
2. Envía `/start`
3. Envía un mensaje de voz diciendo: "Test"
4. Debería responder en 3-5 segundos

---

## 📝 Estructura del Código

```
dante-bot/
├── main.py                 # Bot principal
├── requirements.txt        # Dependencias
├── .env.example           # Variables de entorno
├── .env                   # Variables reales (NO commitar a Git)
├── Procfile               # Para Heroku/Railway
└── README.md              # Este archivo
```

### Funciones Principales:

- `start()` - Comando inicial
- `handle_voice()` - Procesa mensajes de voz (descarga + transcribe)
- `transcribe_voice()` - Convierte audio a texto (Google Speech Recognition)
- `process_with_claude()` - Envía a Claude con contexto DANTE
- `handle_text()` - Procesa mensajes de texto directo
- `error_handler()` - Maneja errores globales

---

## 🔐 Seguridad

- ✅ Variables de entorno en `.env` (NO en el código)
- ✅ `.env` añadido a `.gitignore` (no commitar tokens)
- ✅ API Keys protegidas en variables de entorno de Railway/Render
- ✅ Solo responde a mensajes válidos de Telegram
- ✅ Rate limiting automático de Telegram

**No expongas tu TELEGRAM_TOKEN ni CLAUDE_API_KEY en:**
- Código
- Commits a GitHub
- Logs públicos

---

## 💡 Mejoras Futuras

- [ ] Sintetizar respuestas a voz (text-to-speech)
- [ ] Guardar historial de conversaciones
- [ ] Análisis de sentiment en leads
- [ ] Integración con CRM (Pipedrive, etc.)
- [ ] Comandos personalizados más específicos
- [ ] Base de datos de clientes para contexto mejorado

---

## 📞 Soporte

Si el bot no funciona:

1. Revisa los **logs** (Railway/Render)
2. Verifica que TELEGRAM_TOKEN y CLAUDE_API_KEY sean correctos
3. Intenta localmente primero: `python main.py`
4. Revisa que el webhook esté configurado correctamente

---

## 📄 Licencia

Uso privado de Sergio Delviso (AINCAT)

---

**¡Tu bot está listo! 🚀**

Próximo paso: [Ver instrucciones de Railway arriba](#opción-1-railway--recomendado)
