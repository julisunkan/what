# WhatsApp Bot Creator

A full-stack Progressive Web App (PWA) for creating and managing WhatsApp chatbots. Built with Python Flask, SQLite, and WPPConnect for WhatsApp integration.

## Features

- **User Authentication**: Secure registration and login with password hashing
- **Bot Management**: Create, edit, and delete multiple WhatsApp bots
- **Keyword Rules**: Define keyword-response pairs for intelligent conversations
- **Analytics Dashboard**: Track message statistics and user engagement
- **Progressive Web App**: Installable on mobile devices with offline support
- **WhatsApp Integration**: Connect to WhatsApp using WPPConnect gateway
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
│   └── analytics.py       # Analytics routes
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
├── bot_gateway/           # WhatsApp gateway (Node.js)
│   ├── bot.js
│   ├── package.json
│   └── README.md
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

## WhatsApp Integration

### Setup WhatsApp Gateway (Optional)

The `bot_gateway` folder contains a Node.js application that connects WhatsApp to your Flask API.

#### Prerequisites
- Node.js 18+ installed
- Chrome/Chromium browser (for WPPConnect)

#### Steps

1. Navigate to the bot_gateway folder:
```bash
cd bot_gateway
npm install
```

2. Ensure your Flask app is running

3. Start the WhatsApp gateway:
```bash
npm start
```

4. Scan the QR code with WhatsApp (Settings → Linked Devices)

5. Send a test message to your WhatsApp number

For detailed instructions, see `bot_gateway/README.md`.

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

### Using Ngrok (for WhatsApp Gateway)

If you want to connect the WhatsApp gateway to a local Flask instance:

```bash
ngrok http 5000
```

Update `FLASK_API_URL` in `bot_gateway/bot.js` with the ngrok URL.

## Security Notes

- Passwords are hashed using Werkzeug's secure password hashing
- Session secrets should be set via environment variables in production
- The API endpoint is public - consider adding API key authentication for production use
- SQLite is suitable for development; consider PostgreSQL for production

## Technologies Used

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **PWA**: Service Workers, Web App Manifest
- **WhatsApp**: WPPConnect (Node.js)
- **Deployment**: Replit

## Troubleshooting

### Database not initializing
- Delete `whatsapp_bot.db` and restart the app

### PWA not installing
- Ensure you're accessing via HTTPS (Replit provides this automatically)
- Check browser console for service worker errors

### WhatsApp gateway connection issues
- Verify Flask app is running and accessible
- Check that Chrome/Chromium is installed
- Delete `bot_gateway/tokens` folder and rescan QR code

### Messages not being processed
- Ensure at least one bot is marked as "Active"
- Check that keywords are correctly configured
- Review message logs in the analytics dashboard

## License

MIT License - Feel free to use and modify for your projects.

## Support

For issues or questions, please check the troubleshooting section or review the inline documentation in the code.
