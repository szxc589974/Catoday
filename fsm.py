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

photoChoice = ['https://i.imgur.com/zFmUfzB.jpg','https://i.imgur.com/elFmbF3.jpg','https://i.imgur.com/DWouK24.jpg','https://i.imgur.com/4eCtfdV.jpg','https://i.imgur.com/CHSYUaw.jpg','https://i.imgur.com/fmu6mi2.jpg','https://i.imgur.com/IJb1d5D.jpg','https://i.imgur.com/NpVX1or.jpg','https://i.imgur.com/CGGsbUo.jpg','https://i.imgur.com/QwngCq5.jpg','https://i.imgur.com/Q7C2H6W.jpg','https://i.imgur.com/17WX1Cb.jpg','https://i.imgur.com/kGHEia2.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/MIUMTjM.jpg','https://i.imgur.com/HadFEcM.jpg','https://i.imgur.com/e5L8ZYI.jpg','https://i.imgur.com/BcjDfdq.jpg','https://i.imgur.com/qARyHTH.jpg','https://i.imgur.com/XDDfrzk.jpg','https://i.imgur.com/lGKspNb.jpg','https://i.imgur.com/GxcjzWn.jpg','https://i.imgur.com/kwA4EzR.jpg','https://i.imgur.com/4Zkd6A4.jpg','https://i.imgur.com/TyE7ssH.jpg','https://i.imgur.com/PYWGuyp.jpg','https://i.imgur.com/ddyGO9T.jpg','https://i.imgur.com/ozllp4R.jpg']
age = [15,24]
for i in range(1,19):
    age.append(age[i]+4)

line_bot_api = LineBotApi('onuCCvT4ps0AgZTtjpvqTWkPZMj0j4watDwDOAjhRmREPADoakKvtSx0ycjyeuATh08cxvIf+QsnlDjYJjBb2jGqWwZUBuGy2J76Pe3Wk/RlominSvkxIyFsdOHAOTKVv9+UTP2FxA3i4XbpOKjmLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0514d217b27b5e876c1e1a4b4623b7ea')
GOOGLE_API_KEY = 'AIzaSyDMA-HQJr05I3DJHo4iNQs39rSOUi5EwMA'

#
def askAge(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入貓咪歲數:"))

def convertAge(event):
    covert = age[int(event.message.text)-1]
    replyCovertAge = "轉換成人類歲數為" + str(covert) + "歲"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=replyCovertAge))

def sendPicture(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=random.choice(photoChoice), 
            preview_image_url=random.choice(photoChoice)
        )
    )
def sendLocation(event):
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

def receiveLocation(event):
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
        # 3. 隨機選擇一間醫院
        veterinary_care = random.choice(top20_veterinary_care)
    veterinary_care = top20_veterinary_care[random.choice(above4)]
        # 4. 檢查醫院有沒有照片，有的話會顯示
    print(veterinary_care)
    if veterinary_care.get("photos") is None:
        thumbnail_image_url = None
    else:
            # 根據文件，最多只會有一張照片
        photo_reference = veterinary_care["photos"][0]["photo_reference"]
        thumbnail_image_url = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth=1024".format(GOOGLE_API_KEY, photo_reference)
        # 5. 組裝醫院詳細資訊
    rating = "無" if veterinary_care.get("rating") is None else veterinary_care["rating"]
    address = "沒有資料" if veterinary_care.get("vicinity") is None else veterinary_care["vicinity"]
    details = "評分：{}\n地址：{}".format(rating, address)

        # 6. 取得醫院的 Google map 網址
    map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
        lat=veterinary_care["geometry"]["location"]["lat"],
        long=veterinary_care["geometry"]["location"]["lng"],
        place_id=veterinary_care["place_id"]
    )
        # 使用 Google API End =========

    # 回覆使用 Buttons Template
    Button_Template = TemplateSendMessage(
        alt_text=veterinary_care["name"],
        template=ButtonsTemplate(
            thumbnail_image_url=thumbnail_image_url,
            title=veterinary_care["name"],
            text=details,
            actions=[
                URITemplateAction(
                    label='查看地圖',
                    uri=map_url
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,Button_Template)
