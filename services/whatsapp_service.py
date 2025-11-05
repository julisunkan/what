import os
import requests
from twilio.rest import Client

class WhatsAppService:
    def __init__(self):
        self.provider = os.environ.get('WHATSAPP_PROVIDER', 'twilio')

        if self.provider == 'twilio':
            self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            self.from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

            if self.account_sid and self.auth_token:
                self.client = Client(self.account_sid, self.auth_token)
            else:
                self.client = None

        elif self.provider == 'meta':
            self.access_token = os.environ.get('META_WHATSAPP_TOKEN')
            self.phone_number_id = os.environ.get('META_PHONE_NUMBER_ID')
            self.api_version = os.environ.get('META_API_VERSION', 'v21.0')

    def send_message_twilio(self, to_number, message_body):
        if not self.client:
            raise ValueError('Twilio credentials not configured')

        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'

        message = self.client.messages.create(
            from_=self.from_number,
            body=message_body,
            to=to_number
        )

        return message.sid

    def send_message_meta(self, to_number, message_body):
        if not self.access_token or not self.phone_number_id:
            raise ValueError('Meta WhatsApp credentials not configured')

        to_number = to_number.replace('whatsapp:', '').replace('+', '').replace('-', '')

        url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": message_body
            }
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json().get('messages', [{}])[0].get('id')

    def send_message(self, to_number, message_body):
        if self.provider == 'twilio':
            return self.send_message_twilio(to_number, message_body)
        elif self.provider == 'meta':
            return self.send_message_meta(to_number, message_body)
        else:
            raise ValueError(f'Unknown provider: {self.provider}')

    def is_configured(self):
        if self.provider == 'twilio':
            return bool(self.account_sid and self.auth_token)
        elif self.provider == 'meta':
            return bool(self.access_token and self.phone_number_id)
        return False