# ⚡ QUICKSTART - @DanteAssitBot (5 minutos)

**¿Prisa? Aquí está lo esencial para empezar YA.**

---

## 🎯 Lo que tienes

Estos archivos están listos:
- ✅ `main.py` - Bot completo
- ✅ `requirements.txt` - Dependencias
- ✅ `.env.example` - Variables
- ✅ `Procfile` - Para Railway
- ✅ Documentación completa

---

## 🚀 Opción A: Deploy en Railway (MÁS FÁCIL)

**Tiempo: 10 minutos. Gratuito.**

1. **Ir a:** https://railway.app → Sign up con GitHub
2. **New Project** → Deploy from GitHub → tu repo `dante-bot`
3. **Variables** (pestaña):
   - `TELEGRAM_TOKEN` = Tu token de @BotFather
   - `CLAUDE_API_KEY` = Tu API key de https://console.anthropic.com
   - `APP_URL` = Tu URL de Railway (ej: `https://dante-bot-prod.railway.app`)
4. **Webhook** (en navegador):
   ```
   https://api.telegram.org/botTU_TOKEN/setWebhook?url=https://tu-url-railway/TU_TOKEN
   ```
5. **Listo.** Abre Telegram → @DanteAssitBot → `/start`

📖 **Guía detallada:** Ver `DEPLOYMENT_RAILWAY.md`

---

## 🎮 Opción B: Test Local (primero)

**Tiempo: 3 minutos. Para validar antes de deployar.**

```bash
# 1. Crear carpeta
mkdir dante-bot
cd dante-bot

# 2. Copiar archivos (main.py, requirements.txt, .env.example, etc.)

# 3. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables
cp .env.example .env
# Editar .env con tu TELEGRAM_TOKEN y CLAUDE_API_KEY

# 6. Probar APIs
python test_local.py

# 7. Ejecutar bot
python main.py
```

Deberías ver:
```
INFO:__main__:Iniciando @DanteAssitBot...
INFO:__main__:Iniciando en modo polling (desarrollo)
```

---

## 📱 Usar el Bot

Abre Telegram → Busca **@DanteAssitBot**

Comandos:
- `/start` - Iniciar
- `/help` - Ver ayuda
- `/status` - Estado

Envía un **mensaje de voz** diciendo:
- "Dame el briefing de hoy"
- "Cualifica a este cliente..."
- "Redacta un correo para..."

O **texto directo** con lo que necesites.

---

## 🔧 Variables de Entorno (Necesarias)

```
TELEGRAM_TOKEN=123456:ABC-DEF...
CLAUDE_API_KEY=sk-ant-...
APP_URL=https://tu-url-railway.app  (Solo si es producción)
WEBHOOK_URL=https://api.telegram.org/bot  (Solo si es producción)
```

---

## ❓ Troubleshooting Rápido

**Bot no responde:**
- Verifica TELEGRAM_TOKEN y CLAUDE_API_KEY
- Revisa logs en Railway (pestaña "Logs")

**Error de transcripción de voz:**
- Habla más claro
- Intenta con texto primero

**Error "Webhook no configurado":**
- Ejecuta: `python setup_webhook.py` (necesita .env)
- O configura manualmente la URL en Telegram

---

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| API Key inválida | Regenera en https://console.anthropic.com |
| Bot inactivo | Revisa logs de Railway |
| No descarga voz | Verifica permisos de Telegram API |
| Webhook error | Ejecuta `python setup_webhook.py` |

---

## 📖 Documentación Completa

- `README.md` - Guía completa (todas las opciones)
- `DEPLOYMENT_RAILWAY.md` - Railway paso a paso
- `main.py` - Código comentado

---

## ✨ ¡Listo!

Tu bot está 100% operativo. Elige:

- **Railway en 10 min:** Ver `DEPLOYMENT_RAILWAY.md`
- **Local primero:** `python main.py`
- **Full setup:** Ver `README.md`

**¡A producción! 🚀**
