# WhatsApp Bot Creator

A full-stack Progressive Web App (PWA) for creating and managing WhatsApp chatbots. Built entirely with Python Flask, SQLite, and integrates with WhatsApp via Twilio or Meta's Cloud API.

## Features

- **User Authentication**: Secure registration and login with password hashing
- **Bot Management**: Create, edit, and delete multiple WhatsApp bots
- **Keyword Rules**: Define keyword-response pairs for intelligent conversations
- **Analytics Dashboard**: Track message statistics and user engagement
- **Progressive Web App**: Installable on mobile devices with offline support
- **WhatsApp Integration**: Pure Python integration with Twilio or Meta WhatsApp Cloud API
- **Real-time Logging**: Track all incoming and outgoing messages
- **Bootstrap UI**: Clean, responsive interface with inline alerts

## Project Structure

```
.
├── app.py                  # Main Flask application
├── models/                 # Database models
│   ├── __init__.py
│   ├── user.py            # User model
│   ├── bot.py             # Bot model
│   ├── rule.py            # Rule model
│   └── message_log.py     # Message log model
├── routes/                 # Flask blueprints
│   ├── auth.py            # Authentication routes
│   ├── bots.py            # Bot management routes
│   ├── api.py             # API endpoint for WhatsApp
│   ├── analytics.py       # Analytics routes
│   └── whatsapp.py        # WhatsApp webhook endpoints
├── services/               # Service modules
│   └── whatsapp_service.py # WhatsApp messaging service
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html         # Login/Register page
│   ├── dashboard.html     # Bot management
│   ├── edit_bot.html      # Edit bot and rules
│   └── analytics.html     # Analytics dashboard
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── service-worker.js
│   │   └── sw-register.js
│   ├── icons/             # PWA icons
│   └── manifest.webmanifest
├── WHATSAPP_SETUP.md      # WhatsApp integration guide
└── whatsapp_bot.db        # SQLite database (auto-created)
```

## Installation & Setup

### 1. Clone or Open in Replit

This project is optimized for Replit. Simply click "Run" to start the Flask server.

### 2. Install Python Dependencies

Python dependencies are automatically installed via `pyproject.toml`:
- Flask
- Flask-SQLAlchemy
- Werkzeug
- Twilio (for WhatsApp integration)
- Requests

### 3. Set Environment Variables

The app uses a `SESSION_SECRET` environment variable for session security. This is automatically configured in Replit.

### 4. Run the Flask Application

The Flask server will automatically start on port 5000:

```bash
python app.py
```

Access the web app at: `http://0.0.0.0:5000` or your Replit URL.

### 5. Create Your First Account

1. Open the application in your browser
2. Click "Register" and create a new account
3. Log in with your credentials

### 6. Create Your First Bot

1. From the dashboard, enter a bot name
2. Set a fallback message (sent when no keyword matches)
3. Click "Create Bot"
4. Click "Edit" to add keyword-response rules

### 7. Add Keyword Rules

1. In the bot editor, add keywords and their responses
2. Keywords are matched using case-insensitive substring matching
3. Example: keyword "hello" will match "Hello", "hello there", etc.

## WhatsApp Integration (Pure Python! 🐍)

Your bot can connect to WhatsApp using **100% Python** - no Node.js required!

### Quick Start

You have two options:

**Option 1: Twilio** (Easiest)
- Quick setup with Twilio's WhatsApp sandbox
- Pay-per-message pricing (free trial included)
- Great for testing and production

**Option 2: Meta WhatsApp Cloud API** (Free)
- Free tier: 1,000 conversations/month
- Direct integration with Meta's official API
- Requires Facebook Business account setup

### Setup Steps

1. **Choose your provider** (Twilio or Meta)
2. **Configure environment variables** in Replit Secrets:
   - For Twilio: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
   - For Meta: `META_WHATSAPP_TOKEN`, `META_PHONE_NUMBER_ID`
3. **Set up webhook** in Twilio/Meta console pointing to your Replit URL
4. **Create a bot** in the dashboard with keyword rules
5. **Send a test message** to your WhatsApp number

### Full Documentation

See **[WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)** for complete step-by-step instructions for both providers.

## API Endpoint

### POST `/api/get_response`

Process incoming messages and return bot responses.

**Request:**
```json
{
  "sender": "1234567890",
  "message": "hello"
}
```

**Response:**
```json
{
  "response": "Hi there! How can I help you?"
}
```

**Features:**
- Logs all incoming and outgoing messages
- Matches keywords in bot rules
- Returns fallback message if no keyword matches
- Uses the first active bot in the database

## PWA Features

### Installation

The app is installable as a Progressive Web App:

1. Open the app in Chrome or Safari
2. Look for the "Install" or "Add to Home Screen" option
3. The app will work offline once installed

### Service Worker

Caches static assets for offline access:
- CSS files
- JavaScript files
- Manifest file
- Base routes

## Analytics

View detailed statistics for each bot:
- Total messages processed
- Incoming vs outgoing message counts
- Number of unique users
- Bot activity status

Access analytics at `/analytics`.

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `date_created`: Account creation timestamp

### Bots Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `name`: Bot name
- `fallback_message`: Default response
- `active`: Boolean status

### Rules Table
- `id`: Primary key
- `bot_id`: Foreign key to Bots
- `keyword`: Trigger keyword
- `response`: Bot response

### MessageLog Table
- `id`: Primary key
- `bot_id`: Foreign key to Bots
- `sender`: Message sender identifier
- `direction`: 'incoming' or 'outgoing'
- `message`: Message content
- `timestamp`: Message timestamp

## Production Deployment

### Using Replit

1. Click the "Publish" button in Replit
2. Configure your custom domain (optional)
3. The app will be deployed automatically
4. Update webhook URLs in Twilio/Meta console with your production domain

## Security Notes

- Passwords are hashed using Werkzeug's secure password hashing
- Session secrets should be set via environment variables in production
- Webhook endpoints include signature validation for Twilio and Meta
- All WhatsApp API credentials are stored in Replit Secrets (environment variables)
- SQLite is suitable for development; consider PostgreSQL for production
- Never expose API tokens or app secrets in code or version control

## Technologies Used

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **PWA**: Service Workers, Web App Manifest
- **WhatsApp**: Twilio SDK / Meta WhatsApp Cloud API (Python)
- **Deployment**: Replit

## Troubleshooting

### Database not initializing
- Delete `whatsapp_bot.db` and restart the app

### PWA not installing
- Ensure you're accessing via HTTPS (Replit provides this automatically)
- Check browser console for service worker errors

### WhatsApp integration not working
- Check environment variables are set correctly in Replit Secrets
- Verify webhook URL is correct in Twilio/Meta console
- Make sure webhook signature validation credentials are configured
- Test the webhook endpoint responds with 200 OK

### Messages not being processed
- Ensure at least one bot is marked as "Active"
- Check that keywords are correctly configured
- Review message logs in the analytics dashboard
- Verify webhook endpoints are receiving requests (check workflow logs)

## License

MIT License - Feel free to use and modify for your projects.

## Support

For issues or questions, please check the troubleshooting section or review the inline documentation in the code.
