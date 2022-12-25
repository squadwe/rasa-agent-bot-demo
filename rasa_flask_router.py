import requests

rasa_url = 'http://localhost:5005'
squadwe_url = 'http://localhost:3000'
squadwe_bot_token = '<your agent bot token>'


def send_to_bot(sender, message):
    data = {
        'sender': sender,
        'message': message
    }
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    r = requests.post(f'{rasa_url}/webhooks/rest/webhook',
                      json=data, headers=headers)
    return r.json()[0]['text']


def send_to_squadwe(account, conversation, message):
    data = {
        'content': message
    }
    url = f"{squadwe_url}/api/v1/accounts/{account}/conversations/{conversation}/messages"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{squadwe_bot_token}"}

    r = requests.post(url,
                      json=data, headers=headers)
    return r.json()


from flask import Flask, request
app = Flask(__name__)


@app.route('/rasa', methods=['POST'])
def rasa():
    data = request.get_json()
    message_type = data['message_type']
    message = data['content']
    conversation = data['conversation']['id']
    contact = data['sender']['id']
    account = data['account']['id']

    if(message_type == "incoming"):
        bot_response = send_to_bot(contact, message)
        create_message = send_to_squadwe(
            account, conversation, bot_response)
    return create_message

if __name__ == '__main__':
    app.run(debug=1)
    # print(send_to_squadwe(2,12,'3'))
