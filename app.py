import random
import os

from flask import Flask, request

from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

bot = Bot(ACCESS_TOKEN)


@app.route('/', methods=['GET', 'POST'])
def receive_message():

    print("Someone is trying talk...")

    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")

        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Message ID
                    recipient_id = message['sender']['id']

                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # if user sends any non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def get_message():
    """
    Choose a random message to send to the user
    """
    sample_responses = ["You are stunning!", "We're proud of you.",
                        "Keep on being you!", "We're greatful to know you :)"]

    # return selected item to the user
    return random.choice(sample_responses)


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Invalid verification token'


def send_message(recipient_id, response):
    """
    sends message to user
    """
    bot.send_text_message(recipient_id, response)


if __name__ == '__main__':
    app.run()
