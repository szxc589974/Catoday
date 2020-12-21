# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

import configparser

age = [15,24]
for i in range(1,19):
    age.append(age[i]+4)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('onuCCvT4ps0AgZTtjpvqTWkPZMj0j4watDwDOAjhRmREPADoakKvtSx0ycjyeuATh08cxvIf+QsnlDjYJjBb2jGqWwZUBuGy2J76Pe3Wk/RlominSvkxIyFsdOHAOTKVv9+UTP2FxA3i4XbpOKjmLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0514d217b27b5e876c1e1a4b4623b7ea')

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

# 轉換年齡
@handler.add(MessageEvent, message=TextMessage) #如果收到文字訊息就執行下面程式碼
def convertAge(event):
    
    covert = age[int(event.message.text)-1]
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=covert)
        )

# 轉換年齡
@handler.add(MessageEvent, message=ImageMessage) #如果收到文字訊息就執行下面程式碼
def sendImage(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://drive.google.com/file/d/14A9MElyhhosigX3AEn1RaxH5rhEfJ_1X/view?usp=sharing', preview_image_url='https://drive.google.com/file/d/14A9MElyhhosigX3AEn1RaxH5rhEfJ_1X/view?usp=sharing')
        )

if __name__ == "__main__":
    app.run()


#MessageEvent (信息事件)、FollowEvent (加好友事件)、UnfollowEvent (刪好友事件)、JoinEvent (加入聊天室事件)、LeaveEvent (離開聊天室事件)、MemberJoinedEvent (加入群組事件)、MemberLeftEvent (離開群組事件)
#MessageEvent又依照信息內容再分成TextMessage、ImageMessage、VideoMessage、StickerMessage、FileMessage等等