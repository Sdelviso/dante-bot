# 🚀 Guía Paso a Paso: Desplegar @DanteAssitBot en Railway

**Tiempo estimado: 15 minutos**

Railway es la opción más fácil y rápida para desplegar el bot. Es gratuita para empezar.

---

## ✅ Checklist Previo

Antes de empezar, ten a mano:
- [ ] Tu `TELEGRAM_TOKEN` (de @BotFather)
- [ ] Tu `CLAUDE_API_KEY` (de https://console.anthropic.com/)
- [ ] Cuenta de GitHub (crea una en github.com si no tienes)
- [ ] Los archivos del bot descargados

---

## PASO 1: Crear Repositorio en GitHub

### 1.1 - Crea un repositorio

1. Ve a https://github.com/new
2. **Repository name**: `dante-bot`
3. **Description**: `Bot de Telegram para DANTE - Asistente Inmobiliario`
4. **Public** o **Private** (como prefieras)
5. Haz clic en **"Create repository"**

### 1.2 - Descargar Git

Si no tienes Git instalado:
- Windows: https://git-scm.com/download/win
- macOS: `brew install git`
- Linux: `sudo apt install git`

### 1.3 - Preparar tus archivos

Coloca estos archivos en una carpeta `dante-bot`:

```
dante-bot/
├── main.py
├── requirements.txt
├── .env.example
├── Procfile
└── setup_webhook.py
```

### 1.4 - Inicializar Git

Abre terminal/PowerShell en la carpeta `dante-bot`:

```bash
git init
git add .
git commit -m "Initial commit: DANTE Bot"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/dante-bot.git
git push -u origin main
```

*(Reemplaza `TU_USUARIO` con tu usuario de GitHub)*

**Ahora tus archivos están en GitHub ✅**

---

## PASO 2: Desplegar en Railway

### 2.1 - Crear cuenta en Railway

1. Ve a https://railway.app
2. Haz clic en **"Start Now"** (arriba a la derecha)
3. Haz login con GitHub
   - Autoriza Railway a acceder a tus repositorios
4. Listo!

### 2.2 - Crear un nuevo proyecto

1. En el dashboard de Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub"**
3. Busca y selecciona tu repositorio `dante-bot`
4. Railway detectará automáticamente que es Python
5. Haz clic en **"Deploy"**

### 2.3 - Esperar a que se depliegue

Verás logs como:
```
[...] Installing dependencies
[...] Running on 0.0.0.0:8443
[...] Bot is running
```

**Cuando aparezca una URL verde en la parte superior, ¡está listo!**
(Algo como: `https://dante-bot-prod.railway.app`)

---

## PASO 3: Configurar Variables de Entorno

### 3.1 - Acceder a la pestaña de variables

1. En tu proyecto de Railway, haz clic en la pestaña **"Variables"**
2. Haz clic en **"Add Variable"**

### 3.2 - Añadir variables (una por una)

Añade estas 4 variables:

**1. TELEGRAM_TOKEN**
- Key: `TELEGRAM_TOKEN`
- Value: `Tu_Token_De_BotFather` (ejemplo: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
- Haz clic en **"Add"**

**2. CLAUDE_API_KEY**
- Key: `CLAUDE_API_KEY`
- Value: `sk-ant-Tu_Key_Aqui` (conseguir en https://console.anthropic.com/)
- Haz clic en **"Add"**

**3. APP_URL**
- Key: `APP_URL`
- Value: `https://dante-bot-prod.railway.app` (O la URL que Railway te dio)
- Haz clic en **"Add"**

**4. WEBHOOK_URL**
- Key: `WEBHOOK_URL`
- Value: `https://api.telegram.org/bot` (URL base de Telegram)
- Haz clic en **"Add"**

### 3.3 - Redeploy con las nuevas variables

1. Una vez añadidas las variables, Railway redeploy automáticamente
2. Verás los logs actualizándose
3. Espera a que se complete (verás "Deployment Successful")

---

## PASO 4: Configurar Webhook de Telegram

### 4.1 - Obtener la URL final

En Railway:
1. Abre tu proyecto
2. Copia la URL de arriba (ej: `https://dante-bot-prod.railway.app`)

### 4.2 - Registrar webhook en Telegram

Abre tu navegador e ingresa esta URL (reemplaza los valores):

```
https://api.telegram.org/botTU_TOKEN/setWebhook?url=https://dante-bot-prod.railway.app/TU_TOKEN
```

Ejemplo completo:
```
https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/setWebhook?url=https://dante-bot-prod.railway.app/123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

Presiona Enter. Deberías ver:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

**¡Si ves eso, tu webhook está configurado! ✅**

---

## PASO 5: Probar el Bot

### 5.1 - Envía un mensaje de prueba

1. Abre Telegram
2. Busca **@DanteAssitBot**
3. Envía `/start`
4. Deberías recibir un mensaje de bienvenida

### 5.2 - Prueba con voz

1. Envía un **mensaje de voz** diciendo: "¿Hola DANTE, estás ahí?"
2. El bot debería:
   - Mostrar: "🎤 Escuché: ¿Hola DANTE, estás ahí?"
   - Procesar
   - Responder con una salutación

### 5.3 - Prueba con un skill

Envía un mensaje de voz:
```
"Dame el briefing de hoy con mis tareas y leads"
```

El bot debería generar una respuesta de briefing.

---

## 🔍 Monitoreo en Railway

### Ver logs en tiempo real

1. En tu proyecto de Railway
2. Pestaña **"Logs"** (en la barra lateral)
3. Verás todos los mensajes del bot en tiempo real

### Buscar errores

En los logs, busca líneas rojas como:
```
ERROR: ...
```

Problemas comunes:
- **No se descarga voz**: Revisar permisos de Telegram
- **Claude no responde**: Revisar CLAUDE_API_KEY en variables
- **Webhook no registra**: Revisar que la URL sea correcta

---

## 🚨 Si algo falla

### Bot no responde

1. Revisa logs en Railway (pestaña "Logs")
2. Verifica variables de entorno:
   - TELEGRAM_TOKEN ✓
   - CLAUDE_API_KEY ✓
   - APP_URL ✓
3. Verifica que el webhook esté registrado:
   ```
   https://api.telegram.org/botTU_TOKEN/getWebhookInfo
   ```

### Error de transcripción de voz

- Habla más claro en el mensaje de voz
- Envía audios de 5-30 segundos
- El bot intenta transcribir automáticamente

### Error de API de Claude

1. Verifica tu CLAUDE_API_KEY en console.anthropic.com
2. Asegúrate que tenga créditos
3. Revisa los logs de Railway

---

## 📊 Información de Costos

- **Railway**: Gratuito para los primeros $5 USD/mes, luego costo real (muy económico)
- **Telegram Bot**: Gratuito
- **Claude API**: Pago por uso (~$0.001-0.005 por mensaje)

**Estimado mensual**: $5-10 USD si el bot recibe 100+ mensajes al día

---

## ✨ ¡Éxito!

Tu @DanteAssitBot está en producción y listo para usar.

**Próximas mejoras opcionales:**
- Añadir text-to-speech (respuestas en audio)
- Guardar historial de conversaciones
- Integrar con CRM (Pipedrive, HubSpot)
- Crear comandos personalizados

---

**¿Preguntas?** Revisa los logs en Railway (pestaña "Logs") - ahí aparecerán todos los errores.
