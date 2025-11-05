# WhatsApp Integration Setup Guide

This guide will help you connect your bot to WhatsApp using **Python only** - no Node.js required!

## Choose Your WhatsApp Provider

You have two options for connecting to WhatsApp:

### Option 1: Twilio (Recommended for Beginners)
- **Pros**: Easy setup, reliable, official Twilio support
- **Cons**: Paid service (pay per message after free trial)
- **Best for**: Quick setup, production apps

### Option 2: Meta WhatsApp Cloud API (Free)
- **Pros**: Free tier (1,000 conversations/month), official Meta API
- **Cons**: More setup steps, requires Facebook Business account
- **Best for**: Cost-conscious projects, higher volume

---

## Option 1: Twilio Setup

### Step 1: Create Twilio Account
1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free account
3. You'll get $15 free credit to test

### Step 2: Get Twilio Credentials
1. From your Twilio Console, find:
   - **Account SID**
   - **Auth Token**
2. Go to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Join the Twilio Sandbox by sending the code to the WhatsApp number shown

### Step 3: Configure Environment Variables in Replit
Click on "Secrets" (lock icon) in Replit and add:

```
WHATSAPP_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Step 4: Set Up Webhook in Twilio
1. In Twilio Console, go to **Messaging** → **Settings** → **WhatsApp Sandbox**
2. Under "When a message comes in", enter:
   ```
   https://YOUR-REPLIT-URL/whatsapp/webhook/twilio
   ```
   Replace `YOUR-REPLIT-URL` with your actual Replit app URL
3. Method: **POST**
4. Click **Save**

### Step 5: Test Your Bot
1. Create a bot in the web app (Dashboard → Create New Bot)
2. Add some rules (e.g., keyword: "hello", response: "Hi there!")
3. Make sure the bot is **Active**
4. Send a WhatsApp message to your Twilio number
5. Your bot should respond!

---

## Option 2: Meta WhatsApp Cloud API Setup

### Step 1: Create Facebook Business Account
1. Go to https://business.facebook.com
2. Create a business account (free)

### Step 2: Set Up WhatsApp Business App
1. Go to https://developers.facebook.com/apps
2. Click "Create App"
3. Choose "Business" type
4. Add "WhatsApp" product to your app

### Step 3: Get API Credentials
1. In your app dashboard, go to **WhatsApp** → **API Setup**
2. Find your:
   - **Phone Number ID**
   - **Access Token** (generate a permanent token)
3. Note the **Webhook Verify Token** (create your own secure string)

### Step 4: Configure Environment Variables in Replit
Click on "Secrets" (lock icon) in Replit and add:

```
WHATSAPP_PROVIDER=meta
META_WHATSAPP_TOKEN=your_access_token_here
META_PHONE_NUMBER_ID=your_phone_number_id_here
META_API_VERSION=v21.0
META_VERIFY_TOKEN=your_secure_verify_token_here
META_APP_SECRET=your_app_secret_here
```

**Important**: 
- `META_VERIFY_TOKEN`: Create your own secure random string (e.g., `my_secure_token_xyz123`)
- `META_APP_SECRET`: Found in Meta App Dashboard → Settings → Basic → App Secret (for webhook signature validation)

### Step 5: Set Up Webhook in Meta
1. In Meta App Dashboard, go to **WhatsApp** → **Configuration**
2. Click "Edit" under Webhook
3. Enter:
   - **Callback URL**: `https://YOUR-REPLIT-URL/whatsapp/webhook/meta`
   - **Verify Token**: Use the SAME value you set in `META_VERIFY_TOKEN` above
4. Subscribe to: `messages`
5. Click **Verify and Save**

### Step 6: Add a Phone Number
1. In the WhatsApp dashboard, add and verify your phone number
2. This number will be used to test your bot

### Step 7: Test Your Bot
1. Create a bot in the web app
2. Add keyword rules
3. Make sure the bot is Active
4. Send a WhatsApp message to your business number
5. Bot should respond!

---

## Testing Your Integration

### Test Endpoint
You can test if your WhatsApp service is configured correctly:

```bash
curl -X POST https://YOUR-REPLIT-URL/whatsapp/test \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+1234567890",
    "message": "Test message from bot!"
  }'
```

### Check Bot is Active
1. Go to Dashboard
2. Make sure at least one bot shows **Active** badge
3. Add some keyword rules to that bot

### View Message Logs
1. Go to Analytics page
2. You'll see all incoming and outgoing messages
3. Check if messages are being logged correctly

---

## Troubleshooting

### Messages Not Being Received
- Check that your webhook URL is correct in Twilio/Meta console
- Verify the webhook is accessible (should return 200 OK)
- Make sure your Replit app is running

### Bot Not Responding
- Ensure at least one bot is marked as "Active"
- Check that keywords are spelled correctly (case-insensitive)
- View Analytics to see if messages are being logged

### Twilio Errors
- Verify Account SID and Auth Token are correct
- Check Twilio console for error logs
- Ensure you've joined the sandbox

### Meta API Errors
- Verify Access Token hasn't expired
- Check Phone Number ID is correct
- Ensure webhook is verified in Meta console
- Review Meta's webhook event logs for errors

---

## Production Deployment

### Twilio Production
1. Request production access in Twilio console
2. Get approved WhatsApp sender (your business number)
3. Update `TWILIO_WHATSAPP_NUMBER` to your approved number

### Meta Production
1. Submit your app for review in Meta Business
2. Get your WhatsApp Business Account approved
3. Use production access tokens

---

## Cost Comparison

### Twilio Pricing
- **Sandbox**: Free for testing
- **Production**: ~$0.005 per message (varies by country)
- **Monthly minimum**: None

### Meta Cloud API Pricing
- **Free Tier**: 1,000 user-initiated conversations/month
- **Beyond Free Tier**: ~$0.01 - $0.08 per conversation (varies by country)
- **Monthly minimum**: None

---

## Security Best Practices

1. **Never commit secrets** - Use Replit Secrets only
2. **Use HTTPS** - Replit provides this automatically
3. **Validate webhooks** - Both Twilio and Meta use signature verification
4. **Rate limiting** - Consider adding rate limits to prevent spam
5. **Monitor usage** - Check Twilio/Meta dashboards regularly

---

## Next Steps

1. Choose your provider (Twilio or Meta)
2. Follow the setup steps above
3. Configure environment variables in Replit Secrets
4. Set up webhooks
5. Test with a simple keyword like "hello"
6. Build more complex bot rules!

---

## Support

- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **Meta Docs**: https://developers.facebook.com/docs/whatsapp/cloud-api/
- **Replit Docs**: https://docs.replit.com/

Happy bot building! 🤖💬
