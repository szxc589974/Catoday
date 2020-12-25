# 載入需要的模組
from __future__ import unicode_literals
import os
import json
import requests
import random
import configparser
import fsm
from flask import Flask, request, abort
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

app = Flask(__name__)




# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('onuCCvT4ps0AgZTtjpvqTWkPZMj0j4watDwDOAjhRmREPADoakKvtSx0ycjyeuATh08cxvIf+QsnlDjYJjBb2jGqWwZUBuGy2J76Pe3Wk/RlominSvkxIyFsdOHAOTKVv9+UTP2FxA3i4XbpOKjmLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0514d217b27b5e876c1e1a4b4623b7ea')
GOOGLE_API_KEY = 'AIzaSyDMA-HQJr05I3DJHo4iNQs39rSOUi5EwMA'

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
askage = 0
@handler.add(MessageEvent, message = TextMessage) #如果收到文字訊息就執行下面程式碼
def receiveText(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "年齡":
            fsm.askAge(event)
            askage = 1
        elif event.message.text == "圖片": 
            fsm.sendPicture(event)
        elif event.message.text == "寵物醫院" : # 當使用者意圖為詢問寵物醫院時
            fsm.sendLocation(event)
        elif type(event.message.text) :
            fsm.convertAge(event)
            askage = 0

@handler.add(MessageEvent, message = LocationMessage)
def handle_location_message(event):
    fsm.receiveLocation(event)


                        

if __name__ == "__main__":
    app.run()


#MessageEvent (信息事件)、FollowEvent (加好友事件)、UnfollowEvent (刪好友事件)、JoinEvent (加入聊天室事件)、
#LeaveEvent (離開聊天室事件)、MemberJoinedEvent (加入群組事件)、MemberLeftEvent (離開群組事件)
#MessageEvent又依照信息內容再分成TextMessage、ImageMessage、VideoMessage、StickerMessage、FileMessage等