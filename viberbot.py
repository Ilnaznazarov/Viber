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
    auth_token='50134467aae7e642-993a953a9bfb00f0-46d5087d90cecab8'
))

def allras():  #метод для рассылки любых сообщений
    f=open('USER_ID.txt','r')
    result = f.read().split()
    f.close()
    for x in result:
       viber.send_messages(x, [
       TextMessage(text="Рассылка")
       ])


@app.route('/', methods=['POST']) # метод для ответа на сообщения из вайбер бота
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data())) #для ошибок
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest): # если есть сообщение то проверяет на наличие данного пользователя в списках, если его нет, то добавляет
        message = viber_request.message
        # lets echo back
        allras()
        f=open('USER_ID.txt','r')
        result = f.read().split()
        f.close()
        print (message)
        if (str(viber_request.sender.id) in result):
            viber.send_messages(viber_request.sender.id, [
            TextMessage(text="Вы уже подписчик")
            ])
        else:
            f=open('USER_ID.txt','a')
            f.write(' ' + str(viber_request.sender.id) + ' ')
            viber.send_messages(viber_request.sender.id, [
            TextMessage(text="Теперь вы подписаны")
            ])

        print (message.text)

    return Response(status=200)

if __name__ == "__main__": # запускает flask, неоходимо прежде сделать сертификаты
    context = ('fullchain2.pem', 'custom.key')
    app.run(host='',port=, debug=True, ssl_context=context)
