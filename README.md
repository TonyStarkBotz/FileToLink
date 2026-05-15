# 🚀 CantarellaBots Media Streamer

A high-performance Telegram media streaming and direct link generator bot built with FastAPI and Telethon. Designed for extreme speed.

![Video Background Preview](https://img.shields.io/badge/Aesthetic-Wuthering_Waves-blueviolet?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Telethon](https://img.shields.io/badge/Telethon-26A5E4?style=for-the-badge&logo=telegram)

## ✨ Features

- ⚡ **Ultra High-Speed Streaming**: Optimized multi-worker engine with adaptive chunking and sequential fallbacks for stability.
- 🔄 **Multi-Session Load Balancing**: Distributes download tasks across multiple Telegram user sessions to bypass rate limits.
- 🎨 **Premium UI**: Modern web interface featuring a cinematic **Wuthering Waves video background**, glassmorphism, and responsive design.
- 🔒 **Force Subscribe (FSUB)**: Gated access ensuring users join your Telegram channels before using the bot.
- 🛡️ **Rate Limiting**: Redis-powered (with memory fallback) rate limiting to prevent spam and abuse.
- 📊 **Admin Dashboard**: Built-in logging for new users and file uploads.
- 📁 **Adaptive Content-Type**: Supports streaming for video, audio, and high-quality photo previews.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Telegram Logic**: Telethon (MTProto)
- **Database**: MongoDB (Motor)
- **Cache**: Redis (optional, falls back to memory)
- **Frontend**: HTML5, Vanilla CSS, TailwindCSS, Jinja2 Templates

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/abhinai2244/FILE-TO-LINK-BOT.git
cd FILE-TO-LINK-BOT
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
DATABASE_URL=mongodb+srv://...
BASE_URL=http://localhost:8000
FORCE_SUB_CHANNELS=-100...
CHANNEL_ID=-100...
USER_SESSIONS=string_session1,string_session2
```

### 4. Run the Application
```bash
py -m app.main
```

## 🤖 BotFather Commands

Copy and paste these to [@BotFather](https://t.me/BotFather) to set up your bot's menu:

```text
start - Start the bot
stats - View bot statistics (Admin Only)
broadcast - Broadcast message (Admin Only)
ban - Ban a user (Admin Only)
unban - Unban a user (Admin Only)
```

## 📂 Project Structure

```text
├── app/
│   ├── bot/            # Telegram bot handlers
│   ├── cache/          # Redis and rate limit logic
│   ├── database/       # MongoDB connections and models
│   ├── streamer/       # Core streaming & multi-session engine
│   ├── static/         # CSS, JS, and Background Video
│   ├── templates/      # Jinja2 HTML templates
│   └── main.py         # FastAPI entry point
├── requirements.txt
└── .env
```

## 🤝 Support & Credits

- **Developer**: [@cantarella_wuwa](https://t.me/cantarella_wuwa)
- **Channel**: [@cantarellabots](https://t.me/cantarellabots)

---
*Built with ❤️ for the community.*
