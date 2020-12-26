# 載入需要的模組
from __future__ import unicode_literals
import os
import sys
import configparser
from flask import Flask, request, abort, jsonify, send_file
from dotenv import load_dotenv
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageSendMessage,
    LocationMessage,
    TemplateSendMessage, ButtonsTemplate, URITemplateAction
)
from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message, send_text_message_AI

machine = TocMachine(
    states=[
        'choice',
        'input_age',
        'convert_age',
        'send_picture',
        'send_location',
        'receive_location',
        'Q1',
        'Q2',
        'Q3',
        'Q4',
        'Q5',
        'Q6',
        'Q7',
        'Q8',
        'resultA',
        'resultB',
        'resultC',
        'resultD',
        'resultE',
        'resultF',
        'resultG'
    ],
    transitions=[
        {'trigger': 'advance', 'source': 'user', 'dest': 'choice', 'conditions': 'is_going_to_choice'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'Q1', 'conditions': 'is_going_to_Q1'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'input_age', 'conditions': 'is_going_to_input_age'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'send_picture', 'conditions': 'is_going_to_send_picture'},
        {'trigger': 'advance', 'source': 'choice', 'dest': 'send_location', 'conditions': 'is_going_to_send_location'},
        {'trigger': 'advance', 'source': 'input_age', 'dest': 'convert_age', 'conditions': 'is_going_to_convert_age'},
        {'trigger': 'advance', 'source': 'send_location', 'dest': 'receive_location', 'conditions': 'is_going_to_receive_location'},
        {'trigger': 'advance', 'source': 'Q1', 'dest': 'Q2', 'conditions': 'is_going_to_Q2'},
        {'trigger': 'advance', 'source': 'Q1', 'dest': 'Q3', 'conditions': 'is_going_to_Q3'},
        {'trigger': 'advance', 'source': 'Q2', 'dest': 'Q4', 'conditions': 'is_going_to_Q4'},
        {'trigger': 'advance', 'source': 'Q2', 'dest': 'resultC', 'conditions': 'is_going_to_resultC'},
        {'trigger': 'advance', 'source': 'Q3', 'dest': 'Q5', 'conditions': 'is_going_to_Q5'},
        {'trigger': 'advance', 'source': 'Q3', 'dest': 'Q6', 'conditions': 'is_going_to_Q6'},
        {'trigger': 'advance', 'source': 'Q4', 'dest': 'resultA', 'conditions': 'is_going_to_resultA'},
        {'trigger': 'advance', 'source': 'Q4', 'dest': 'resultB', 'conditions': 'is_going_to_resultB'},
        {'trigger': 'advance', 'source': 'Q5', 'dest': 'resultE', 'conditions': 'is_going_to_resultE'},
        {'trigger': 'advance', 'source': 'Q5', 'dest': 'resultD', 'conditions': 'is_going_to_resultD'},
        {'trigger': 'advance', 'source': 'Q6', 'dest': 'Q7', 'conditions': 'is_going_to_Q7'},
        {'trigger': 'advance', 'source': 'Q6', 'dest': 'Q8', 'conditions': 'is_going_to_Q8'},
        {'trigger': 'advance', 'source': 'Q7', 'dest': 'resultF', 'conditions': 'is_going_to_resultF'},
        {'trigger': 'advance', 'source': 'Q7', 'dest': 'resultE', 'conditions': 'is_going_to_resultE'},
        {'trigger': 'advance', 'source': 'Q8', 'dest': 'resultG', 'conditions': 'is_going_to_resultG'},
        {'trigger': 'advance', 'source': 'Q8', 'dest': 'resultF', 'conditions': 'is_going_to_resultF'}
        {
            'trigger': 'go_back',
            'source': [
                'choice',
                'input_age',
                'convert_age',
                'send_picture',
                'send_location',
                'receive_location',
                'Q1',
                'Q2',
                'Q3',
                'Q4',
                'Q5',
                'Q6',
                'Q7',
                'Q8',
                'resultA',
                'resultB',
                'resultC',
                'resultD',
                'resultE',
                'resultF',
                'resultG'
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)       
        
app = Flask(__name__, static_url_path='')


# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('onuCCvT4ps0AgZTtjpvqTWkPZMj0j4watDwDOAjhRmREPADoakKvtSx0ycjyeuATh08cxvIf+QsnlDjYJjBb2jGqWwZUBuGy2J76Pe3Wk/RlominSvkxIyFsdOHAOTKVv9+UTP2FxA3i4XbpOKjmLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0514d217b27b5e876c1e1a4b4623b7ea')
GOOGLE_API_KEY = 'AIzaSyDMA-HQJr05I3DJHo4iNQs39rSOUi5EwMA'

mode = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = handler.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')

        if mode == 1:
            if event.message.text.lower() == '功能總覽':
                mode = 0
                send_text_message(event.reply_token, '返回功能總覽')
                continue
            else:
                send_text_message_AI(event.reply_token, event.message.text)
                continue
        else:
            if event.message.text.lower() == 'chat':
                mode = 1
                send_text_message(event.reply_token, '進入聊天模式，隨時輸入『功能總覽』可返回功能總覽')
                continue
            else:
                response = machine.advance(event)


        if response == False:
#            if event.message.text.lower() == 'fsm':
#                send_image_message(event.reply_token, '')
            if machine.state != 'user' and event.message.text.lower() == '功能總覽':
                send_text_message(event.reply_token, '輸入『功能總覽』有些功能或許能幫到您喔!。\n隨時輸入『chat』可以機器人聊天。\n隨時輸入『fsm』可以得到狀態圖。')
                machine.go_back()
            elif machine.state == 'user':
                send_text_message(event.reply_token, '輸入『功能總覽』有些功能或許能幫到您喔!。\n隨時輸入『chat』可以機器人聊天。\n隨時輸入『fsm』可以得到狀態圖。')
            elif machine.state == 'Q1' or machine.state == 'Q2' or machine.state == 'Q3'or machine.state == 'Q4'or machine.state == 'Q5'or machine.state == 'Q6'or machine.state == 'Q7'or machine.state == 'Q8'or machine.state == 'resultA'or machine.state == 'resultB'or machine.state == 'resultC'or machine.state == 'resultD'or machine.state == 'resultE'or machine.state == 'resultF'or machine.state == 'resultG':
                send_text_message(event.reply_token, '請回答『是』或『否』')
            elif machine.state == 'choice':
                send_text_message(event.reply_token, '請輸入『貓咪肥胖指數』或『轉換年齡』或『想看療癒照片』或『尋找附近動物醫院』')
            elif machine.state == 'input_age':
                send_text_message(event.reply_token, '請輸入一個整數')
            elif machine.state == 'send_location':
                send_text_message(event.reply_token, '請傳送您的位置，謝謝!')

    return 'OK'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    app.run()




#MessageEvent (信息事件)、FollowEvent (加好友事件)、UnfollowEvent (刪好友事件)、JoinEvent (加入聊天室事件)、
#LeaveEvent (離開聊天室事件)、MemberJoinedEvent (加入群組事件)、MemberLeftEvent (離開群組事件)
#MessageEvent又依照信息內容再分成TextMessage、ImageMessage、VideoMessage、StickerMessage、FileMessage等