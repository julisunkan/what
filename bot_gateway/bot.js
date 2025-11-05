const wppconnect = require('@wppconnect-team/wppconnect');
const axios = require('axios');

const FLASK_API_URL = process.env.FLASK_API_URL || 'http://127.0.0.1:5000';

async function start() {
  try {
    console.log('Starting WhatsApp Bot Gateway...');
    
    const client = await wppconnect.create({
      session: 'wa-bot-session',
      catchQR: (base64Qr, asciiQR) => {
        console.log('\n=================================');
        console.log('Scan the QR code below with WhatsApp:');
        console.log(asciiQR);
        console.log('=================================\n');
      },
      statusFind: (statusSession, session) => {
        console.log('Status:', statusSession);
      },
      headless: true,
      devtools: false,
      useChrome: true,
      debug: false,
      logQR: true,
    });

    console.log('WhatsApp client connected successfully!');

    client.onMessage(async (message) => {
      try {
        if (message.isGroupMsg) {
          console.log('Ignoring group message');
          return;
        }

        console.log(`\nReceived message from ${message.from}: ${message.body}`);

        const response = await axios.post(`${FLASK_API_URL}/api/get_response`, {
          sender: message.from,
          message: message.body
        });

        const botResponse = response.data.response;
        console.log(`Sending response: ${botResponse}`);

        await client.sendText(message.from, botResponse);
        console.log('Response sent successfully!');

      } catch (error) {
        console.error('Error processing message:', error.message);
        
        try {
          await client.sendText(
            message.from,
            'Sorry, there was an error processing your message. Please try again later.'
          );
        } catch (sendError) {
          console.error('Error sending error message:', sendError.message);
        }
      }
    });

    console.log('\nBot is running and listening for messages...');

  } catch (error) {
    console.error('Failed to start WhatsApp bot:', error);
    process.exit(1);
  }
}

start();
