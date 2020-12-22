# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import *

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

"""
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
"""
@handler.add(MessageEvent, message=TextMessage) #如果收到文字訊息就執行下面程式碼
def convertAge(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "年齡":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入歲數:"))
        elif event.message.text == "圖片": 
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i.imgur.com/zFmUfzB.jpg', preview_image_url='https://i.imgur.com/zFmUfzB.jpg'))
        elif type(event.message.text) :
            covert = age[int(event.message.text)-1]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=covert))
        elif event.message.text == "寵物醫院": # 當使用者意圖為詢問午餐時
            # 建立一個 button 的 template
            buttons_template_message = TemplateSendMessage(
                alt_text="Please tell me where you are",
                template=ButtonsTemplate(
                    text="Please tell me where you are",
                    actions=[
                        URITemplateAction(
                            label="Send my location",
                            uri="line://nv/location"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_template_message)

if __name__ == "__main__":
    app.run()


#MessageEvent (信息事件)、FollowEvent (加好友事件)、UnfollowEvent (刪好友事件)、JoinEvent (加入聊天室事件)、LeaveEvent (離開聊天室事件)、MemberJoinedEvent (加入群組事件)、MemberLeftEvent (離開群組事件)
#MessageEvent又依照信息內容再分成TextMessage、ImageMessage、VideoMessage、StickerMessage、FileMessage等等



"""
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 獲取使用者的經緯度
    lat = event.message.latitude
    long = event.message.longitude

    # 使用 Google API Start =========
    # 1. 搜尋附近餐廳
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(GOOGLE_API_KEY, lat, long)
    nearby_results = requests.get(nearby_url)
    # 2. 得到最近的20間餐廳
    nearby_restaurants_dict = nearby_results.json()
    top20_restaurants = nearby_restaurants_dict["results"]
    ## CUSTOMe choose rate >= 4
    res_num = (len(top20_restaurants)) ##20
    above4=[]
    for i in range(res_num):
        try:
            if top20_restaurants[i]['rating'] > 3.9:
                #print('rate: ', top20_restaurants[i]['rating'])
                above4.append(i)
        except:
            KeyError
    if len(above4) < 0:
        print('no 4 start resturant found')
    # 3. 隨機選擇一間餐廳
        restaurant = random.choice(top20_restaurants)
    restaurant = top20_restaurants[random.choice(above4)]
    # 4. 檢查餐廳有沒有照片，有的話會顯示
    if restaurant.get("photos") is None:
        thumbnail_image_url = None
    else:
        # 根據文件，最多只會有一張照片
        photo_reference = restaurant["photos"][0]["photo_reference"]
        thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=1024".format(GOOGLE_API_KEY, photo_reference)
    # 5. 組裝餐廳詳細資訊
    rating = "無" if restaurant.get("rating") is None else restaurant["rating"]
    address = "沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
    details = "南瓜評分：{}\n南瓜地址：{}".format(rating, address)

    # 6. 取得餐廳的 Google map 網址
    map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
        lat=restaurant["geometry"]["location"]["lat"],
        long=restaurant["geometry"]["location"]["lng"],
        place_id=restaurant["place_id"]
    )
"""