from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
import logging
import time

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

logger = logging.getLogger("app")

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='PythonSampleBot',
    avatar='https://demotivation.ru/wp-content/uploads/2020/11/s1200-2-9.jpg',
    auth_token='='
))

def allras(textzabbix):
    f=open('USER_ID.txt','r')
    result = f.read().split()
    f.close()
    for x in result:
       viber.send_messages(x, [
       TextMessage(text=textzabbix)
       ])

@app.route('/postzabbix', methods=['POST'])
def zabbix_post():
    request_data = request.get_json()

    print ('text-'+request_data['text']+'-')
    print ('id-'+ request_data['chat_id']+'-')
    if (request_data['chat_id']=='all'):
        allras(request_data['text'])
    else:
        viber.send_messages(request_data['chat_id'], [
            TextMessage(text=request_data['text'])
            ])

    return Response(response='{"ok":true}', status=200, content_type='application/json')

@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())
    
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back

        f=open('USER_ID.txt','r')
        result = f.read().split()
        f.close()
        print (message.text)
        if (str(viber_request.sender.id) in result):
            if (message.text=='id' or message.text=='Id' or message.text=='ID' or message.text=='iD'):
                viber.send_messages(viber_request.sender.id, [
                TextMessage(text=viber_request.sender.id)
                ])
            else:
                viber.send_messages(viber_request.sender.id, [
                TextMessage(text="Вы уже подписчик")
                ])
        else:
            f=open('USER_ID.txt','a')
            f.write(' ' + str(viber_request.sender.id) + ' ')
            viber.send_messages(viber_request.sender.id, [
            TextMessage(text="Теперь вы подписаны")
            ])

    return Response(status=200)

if __name__ == "__main__":
    context = ('fullchain2.pem', 'custom.key')
    app.run(host='',port=443, debug=True, ssl_context=context)

    




