# 🎥 Telegram Direct Media Link Generator

A high-performance FastAPI and Telethon-based bot that generates direct download and streaming links for Telegram media without local storage.

## ✨ Features
- **Instant Links**: Generate links for any file up to 4GB.
- **Multi-Session Support**: Load balance across multiple Telegram sessions for uncapped speeds.
- **Streaming Support**: Watch videos directly in players like VLC or MX Player.
- **Force Subscribe**: Ensure users join your channel before using the bot.
- **Admin Dashboard**: Web-based panel to monitor stats and manage users.

## 🚀 Deployment

### Heroku
1. Connect your GitHub repo to Heroku.
2. Set your Config Vars (Environment Variables) in the Heroku Dashboard.
3. Scale your dynos: `heroku ps:scale web=1`.

## 📜 Credits
- **Channel**: [@cantarellabots](https://t.me/cantarellabots)
- **Developer**: [@cantarella_wuwa](https://t.me/cantarella_wuwa)

---
Made with ❤️ using Telethon & FastAPI.
