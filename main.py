# 載入需要的模組
from __future__ import unicode_literals
import os
import json
import requests
import random
import configparser
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


age = [15,24]
for i in range(1,19):
    age.append(age[i]+4)

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

@handler.add(MessageEvent, message = TextMessage) #如果收到文字訊息就執行下面程式碼
def convertAge(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "年齡":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入歲數:"))
        elif event.message.text == "圖片": 
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/zFmUfzB.jpg', 
                    preview_image_url='https://i.imgur.com/zFmUfzB.jpg'
                )
            )
        elif event.message.text == "寵物醫院" : # 當使用者意圖為詢問寵物醫院時
            Button_Template = TemplateSendMessage(
                alt_text='Please tell me where you are',
                template=ButtonsTemplate(
                    title='Send Location',
                    text='請告訴我你所在的位置!',
                    actions=[
                        URITemplateAction(
                            label='Send my location',
                            uri='line://nv/location'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,Button_Template)

        elif type(event.message.text) :
            covert = age[int(event.message.text)-1]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=covert))


@handler.add(MessageEvent, message = LocationMessage)
def handle_location_message(event):
    # 獲取使用者的經緯度
    lat = event.message.latitude
    long = event.message.longitude

    # 使用 Google API Start =========
    # 1. 搜尋附近寵物醫院
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=veterinary_care&language=zh-TW".format(GOOGLE_API_KEY, lat, long)
    nearby_results = requests.get(nearby_url)
    # 2. 得到最近的20間醫院
    nearby_veterinary_care_dict = nearby_results.json()
    top20_veterinary_care = nearby_veterinary_care_dict["results"]

        ## CUSTOMe choose rate >= 4
    veterinary_care_num = (len(top20_veterinary_care)) ##20
    above4=[]
    for i in range(veterinary_care_num):
        try:
            if top20_veterinary_care[i]['rating'] > 4.2 :
                above4.append(i)
        except:
            KeyError

    if len(above4) < 0:
        print('no 4 start resturant found')
        # 3. 隨機選擇一間餐廳
        veterinary_care = random.choice(top20_veterinary_care)
    veterinary_care = top20_veterinary_care[random.choice(above4)]
        # 4. 檢查餐廳有沒有照片，有的話會顯示
    print(veterinary_care)
    if veterinary_care.get("photos") is None:
        thumbnail_image_url = None
    else:
            # 根據文件，最多只會有一張照片
        photo_reference = veterinary_care["photos"][0]["photo_reference"]
        thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=1024".format(GOOGLE_API_KEY, photo_reference)
        # 5. 組裝餐廳詳細資訊
    rating = "無" if veterinary_care.get("rating") is None else veterinary_care["rating"]
    address = "沒有資料" if veterinary_care.get("vicinity") is None else veterinary_care["vicinity"]
    details = "南瓜評分：{}\n南瓜地址：{}".format(rating, address)

        # 6. 取得餐廳的 Google map 網址
    map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
        lat=veterinary_care["geometry"]["location"]["lat"],
        long=veterinary_care["geometry"]["location"]["lng"],
        place_id=veterinary_care["place_id"]
    )
        # 使用 Google API End =========

    # 回覆使用 Buttons Template
    buttons_template_message = TemplateSendMessage(
    alt_text=veterinary_care["name"],
    template=ButtonsTemplate(
            thumbnail_image_url=thumbnail_image_url,
            title=veterinary_care["name"],
            text=details,
            actions=[
                URITemplateAction(
                    label='查看南瓜地圖',
                    uri=map_url
                ),
            ]
        )
    )

                        

if __name__ == "__main__":
    app.run()


#MessageEvent (信息事件)、FollowEvent (加好友事件)、UnfollowEvent (刪好友事件)、JoinEvent (加入聊天室事件)、
#LeaveEvent (離開聊天室事件)、MemberJoinedEvent (加入群組事件)、MemberLeftEvent (離開群組事件)
#MessageEvent又依照信息內容再分成TextMessage、ImageMessage、VideoMessage、StickerMessage、FileMessage等