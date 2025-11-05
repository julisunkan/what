# WhatsApp Bot Gateway

This folder contains the Node.js gateway that connects WhatsApp to your Flask bot backend using WPPConnect.

## Setup Instructions

### 1. Install Dependencies

Navigate to this folder and install the required packages:

```bash
cd bot_gateway
npm install
```

### 2. Configure the Flask API URL

By default, the gateway connects to `http://127.0.0.1:5000`. If your Flask app runs on a different URL, set the environment variable:

```bash
export FLASK_API_URL=http://your-flask-url:5000
```

### 3. Run the Gateway

Start the WhatsApp gateway:

```bash
npm start
```

### 4. Scan QR Code

When you run the gateway for the first time, a QR code will appear in the terminal. Scan it with your WhatsApp mobile app:

1. Open WhatsApp on your phone
2. Go to Settings → Linked Devices
3. Click "Link a Device"
4. Scan the QR code displayed in the terminal

### 5. Test the Bot

Once connected, send a message to your WhatsApp number from another phone. The bot will:

1. Receive the message
2. Send it to your Flask API at `/api/get_response`
3. Get the bot's response
4. Send the response back via WhatsApp

## How It Works

1. **WPPConnect** establishes a connection to WhatsApp Web
2. When a message is received, it's sent to the Flask API
3. The Flask app checks the bot's rules and returns a response
4. The gateway sends the response back to the WhatsApp user

## Notes

- Only direct messages are processed (group messages are ignored)
- The session is saved in the `tokens` folder for persistent login
- Make sure your Flask app is running before starting the gateway
- For production use, consider using ngrok or a similar service to expose your Flask app publicly

## Troubleshooting

- **QR code not appearing**: Make sure Chrome/Chromium is installed on your system
- **Connection fails**: Check that your Flask app is running and accessible
- **Session expired**: Delete the `tokens` folder and restart to scan a new QR code
