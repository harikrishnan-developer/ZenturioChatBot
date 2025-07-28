# 🚀 Quick Telegram Bot Deployment on Render

## Problem Solved
Your original bot used **polling** which doesn't work on Render. This solution uses **webhooks** which work perfectly on cloud platforms.

## Files Created
- [`telegram_bot_webhook.py`](telegram_bot_webhook.py) - Webhook version of your bot
- [`render.yaml`](render.yaml) - Render configuration
- [`Dockerfile`](Dockerfile) - Docker setup
- [`set_webhook.py`](set_webhook.py) - Manual webhook management
- [`.env.example`](.env.example) - Environment variables template

## 🎯 Quick Deploy Steps

### 1. Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. New → Web Service
3. Connect your GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python telegram_bot_webhook.py`

### 2. Set Environment Variables
```
TELEGRAM_TOKEN=your_bot_token
WEBHOOK_URL=https://your-service-name.onrender.com/webhook
BACKEND_URL=https://your-backend-service.onrender.com/ask
GEMINI_API_KEY=your_gemini_key
MONGO_URI=your_mongodb_atlas_connection_string
SENDER_EMAIL=haribro00123@gmail.com
SENDGRID_API_KEY=your_sendgrid_api_key
```

### 3. Deploy & Test
1. Deploy the service
2. Visit `https://your-service-name.onrender.com/health`
3. Test bot with `/start` command

## 🔧 Alternative Free Hosting Options

If Render doesn't work for you:

### Railway.app
- Similar to Render
- Good free tier
- Easy deployment

### Fly.io
- Docker-based deployment
- Free tier available
- Good performance

### Heroku Alternatives
- Cyclic.sh
- Vercel (for serverless functions)
- Netlify Functions

## 🆘 Troubleshooting

### Bot Not Responding
```bash
# Check webhook status
python set_webhook.py
```

### Manual Webhook Setup
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
     -d "url=https://your-service.onrender.com/webhook"
```

### Common Issues
- ❌ **Wrong webhook URL**: Must end with `/webhook`
- ❌ **Service sleeping**: Render free tier sleeps after 15min
- ❌ **Wrong backend URL**: Update to your deployed backend
- ❌ **Missing env vars**: Check all required variables are set
- ❌ **Email not working**: Render blocks SMTP; use Mailgun API instead (configure `MAILGUN_API_KEY` and `MAILGUN_DOMAIN`)

## 💡 Pro Tips

1. **Keep services awake**: Use a service like UptimeRobot to ping your bot every 5 minutes
2. **Monitor logs**: Check Render dashboard for errors
3. **Test locally first**: Run `python telegram_bot_webhook.py` locally to test
4. **Use ngrok for testing**: Expose local webhook for development

## 📞 Need Help?

1. Check the detailed [deployment guide](TELEGRAM_BOT_DEPLOYMENT.md)
2. Review Render service logs
3. Test webhook with `python set_webhook.py`
4. Verify all environment variables are correct

---
**Your bot will now work on Render! 🎉**