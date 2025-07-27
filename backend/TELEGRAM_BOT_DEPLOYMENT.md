# Telegram Bot Deployment Guide for Render

This guide will help you deploy your Telegram bot on Render using webhooks instead of polling.

## Files Created

1. **`telegram_bot_webhook.py`** - Webhook-based version of your Telegram bot
2. **`render.yaml`** - Render service configuration
3. **`Dockerfile`** - Docker configuration for deployment
4. **This deployment guide**

## Step-by-Step Deployment Instructions

### 1. Prepare Your Repository

Make sure all the new files are in your `backend/` directory:
- `telegram_bot_webhook.py`
- `render.yaml`
- `Dockerfile`
- `requirements.txt` (already exists)

### 2. Create a New Render Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `telegram-bot-webhook` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python telegram_bot_webhook.py`

### 3. Set Environment Variables

In your Render service settings, add these environment variables:

#### Required Variables:
- **`TELEGRAM_TOKEN`**: Your bot token from @BotFather
- **`WEBHOOK_URL`**: `https://your-service-name.onrender.com/webhook`
- **`BACKEND_URL`**: Your deployed backend URL (e.g., `https://your-backend.onrender.com/ask`)

#### Optional Variables (if using these features):
- **`GEMINI_API_KEY`**: Your Google Gemini API key
- **`MONGO_URI`**: Your MongoDB connection string
- **`SENDER_EMAIL`**: Email for sending notifications
- **`SENDER_PASSWORD`**: App password for email

### 4. Deploy the Service

1. Click "Create Web Service"
2. Wait for the deployment to complete
3. Your bot webhook will be available at: `https://your-service-name.onrender.com`

### 5. Set the Webhook URL

The webhook will be automatically set when your service starts up. You can verify it's working by:

1. Check the deployment logs for "Webhook set successfully!"
2. Visit `https://your-service-name.onrender.com/health` to verify the service is running
3. Test your bot by sending a message

## Important Notes

### Webhook URL Format
Your webhook URL should be: `https://your-service-name.onrender.com/webhook`

Replace `your-service-name` with your actual Render service name.

### Backend URL Configuration
Make sure to update the `BACKEND_URL` environment variable to point to your deployed backend service, not localhost.

### Free Tier Limitations
- Render free tier services sleep after 15 minutes of inactivity
- They take ~30 seconds to wake up when receiving a request
- Consider upgrading to a paid plan for production use

### Troubleshooting

#### Bot Not Responding
1. Check Render service logs for errors
2. Verify all environment variables are set correctly
3. Ensure webhook URL is accessible: `https://your-service-name.onrender.com/webhook`
4. Check that your backend service is running and accessible

#### Webhook Errors
1. Verify the webhook URL format is correct
2. Check that the service is deployed and running
3. Look for error messages in the deployment logs

#### Rate Limiting
The bot includes built-in rate limiting to prevent Telegram API limits. If you're still hitting limits:
1. Increase `RATE_LIMIT_SECONDS` in the code
2. Reduce the `edit_interval` for message updates

## Testing Your Deployment

1. **Health Check**: Visit `https://your-service-name.onrender.com/health`
2. **Root Endpoint**: Visit `https://your-service-name.onrender.com/`
3. **Bot Test**: Send `/start` to your bot on Telegram
4. **Message Test**: Send a government service question to your bot

## Alternative: Manual Webhook Setup

If automatic webhook setup fails, you can set it manually:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-service-name.onrender.com/webhook"}'
```

Replace `<YOUR_BOT_TOKEN>` with your actual bot token.

## Monitoring

- Check Render dashboard for service health
- Monitor logs for any errors or issues
- Set up alerts for service downtime if needed

## Cost Optimization

For free hosting, consider:
1. Using Render's free tier (with sleep limitations)
2. Railway.app free tier
3. Heroku alternatives like Fly.io
4. Self-hosting on a VPS

## Security Best Practices

1. Never commit tokens or secrets to your repository
2. Use environment variables for all sensitive data
3. Regularly rotate your bot token if compromised
4. Monitor your bot for unusual activity

## Support

If you encounter issues:
1. Check Render documentation
2. Review Telegram Bot API documentation
3. Check the deployment logs for specific error messages
4. Verify all environment variables are correctly set