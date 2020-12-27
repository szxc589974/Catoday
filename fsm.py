from transitions.extensions import GraphMachine
import os
import json
import requests
import random
import configparser
from flask import Flask, jsonify, request, abort, send_file
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,LocationMessage,MessageTemplateActionTemplateSendMessage, ButtonsTemplate, URITemplateAction

from utils import send_text_message, send_button_message, send_image_message

line_bot_api = LineBotApi('onuCCvT4ps0AgZTtjpvqTWkPZMj0j4watDwDOAjhRmREPADoakKvtSx0ycjyeuATh08cxvIf+QsnlDjYJjBb2jGqWwZUBuGy2J76Pe3Wk/RlominSvkxIyFsdOHAOTKVv9+UTP2FxA3i4XbpOKjmLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0514d217b27b5e876c1e1a4b4623b7ea')
GOOGLE_API_KEY = 'AIzaSyDMA-HQJr05I3DJHo4iNQs39rSOUi5EwMA'

photoChoice = ['https://i.imgur.com/zFmUfzB.jpg','https://i.imgur.com/elFmbF3.jpg','https://i.imgur.com/DWouK24.jpg','https://i.imgur.com/4eCtfdV.jpg','https://i.imgur.com/CHSYUaw.jpg','https://i.imgur.com/fmu6mi2.jpg','https://i.imgur.com/IJb1d5D.jpg','https://i.imgur.com/NpVX1or.jpg','https://i.imgur.com/CGGsbUo.jpg','https://i.imgur.com/QwngCq5.jpg','https://i.imgur.com/Q7C2H6W.jpg','https://i.imgur.com/17WX1Cb.jpg','https://i.imgur.com/kGHEia2.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/MIUMTjM.jpg','https://i.imgur.com/HadFEcM.jpg','https://i.imgur.com/e5L8ZYI.jpg','https://i.imgur.com/BcjDfdq.jpg','https://i.imgur.com/qARyHTH.jpg','https://i.imgur.com/XDDfrzk.jpg','https://i.imgur.com/lGKspNb.jpg','https://i.imgur.com/GxcjzWn.jpg','https://i.imgur.com/kwA4EzR.jpg','https://i.imgur.com/4Zkd6A4.jpg','https://i.imgur.com/TyE7ssH.jpg','https://i.imgur.com/PYWGuyp.jpg','https://i.imgur.com/ddyGO9T.jpg','https://i.imgur.com/ozllp4R.jpg']
age = [15,24]
for i in range(1,19):
    age.append(age[i]+4)

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    def is_going_to_choice(self,event):
        text = event.message.text
        return text.lower() == '功能總覽'

    def on_enter_choice(self,event):

        alt_text = '功能總覽'
        title = '功能總覽'
        text = '請選擇以下功能:'
        btn = [
            MessageTemplateAction(
                label = '貓咪肥胖指數',
                text ='貓咪肥胖指數' #go to Q1
            ),
            MessageTemplateAction(
                label = '轉換年齡',
                text = '轉換年齡' #go to input_age
            ),
            MessageTemplateAction(
                label = '想看療癒照片',
                text = '想看療癒照片' #go to send_picture
            ),
            MessageTemplateAction(
                label = '尋找附近動物醫院',
                text = '尋找附近動物醫院' #go to send_location
            )
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)


    def is_going_to_input_age(self,event):
        text = event.message.text
        if text == '轉換年齡':
            return True
        return False

    def on_enter_input_age(self,event):
        send_text_message(event.reply_token,'請輸入貓咪年齡(歲數):')

    def is_going_to_convert_age(self,event):
        text = event.message.text
        if text.lower().isnumeric():
            return True
        return False

    def on_enter_convert_age(self,event):
        covert = age[int(event.message.text)-1]
        replyCovertAge = "轉換成人類歲數為" + str(covert) + "歲"
        send_text_message(event.reply_token,replyCovertAge)

    def is_going_to_send_picture(self,event):
        text = event.message.text
        if text == '想看療癒照片':
            return True
        return False

    def on_enter_send_picture(self,event):
        send_image_message(event.reply_token,random.choice(photoChoice))

    def is_going_to_send_location(self,event):
        text = event.message.text
        if text == '尋找附近動物醫院':
            return True
        return False

    def on_enter_send_location(self,event):
        alt_text = 'Send Location'
        title = 'Send Location'
        text = '請告訴我你所在的位置!'
        btn = URITemplateAction(label='Send my location',uri='line://nv/location')
        send_button_message(event.reply_token,alt_text, title, text, btn)
    
    def is_going_to_receive_location(self,event):
        if latitude and longitude:
            return True
        return False

    def on_enter_receive_location(self,event):
        # 獲取使用者的經緯度
        lat = event.message.latitude
        long = event.message.longitude

        # 1. 搜尋附近寵物醫院
        nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=veterinary_care&language=zh-TW".format(GOOGLE_API_KEY, lat, long)
        nearby_results = requests.get(nearby_url)
        # 2. 得到最近的20間醫院
        nearby_veterinary_care_dict = nearby_results.json()
        top20_veterinary_care = nearby_veterinary_care_dict["results"]

            ## CUSTOMe choose rate >= 4.2
        veterinary_care_num = (len(top20_veterinary_care))
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


    def is_going_to_Q1(self,event):
        text = event.message.text
        if text == '貓咪肥胖指數':
            return True
        return False

    def on_enter_Q1(self,event):
        alt_text = '問題一'
        title = '問題一'
        text = '逆著毛髮方向，移動指尖你能輕易摸到牠的胸腔嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to Q2
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to Q3
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)
    
    def is_going_to_Q2(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_Q2(self,event):
        alt_text = '問題二'
        title = '問題二'
        text = '逆著毛髮方向，移動指尖你能輕易摸到牠的脊椎嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to Q4
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to C
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_Q3(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_Q3(self,event):
        alt_text = '問題三'
        title = '問題三'
        text = '逆著毛髮方向，移動指尖你能輕易摸到牠的肋骨嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to Q5
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to Q6
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)
        
    def is_going_to_Q4(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_Q4(self,event):
        alt_text = '問題四'
        title = '問題四'
        text = '逆著毛髮方向，移動指尖你能輕易摸到牠的肩胛骨和髖骨嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to A
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to B
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_Q5(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_Q5(self,event):
        global isEnterQ5 = True
        alt_text = '問題五'
        title = '問題五'
        text = '肋骨上是否有一層脂肪'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to E
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to D
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_Q6(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_Q6(self,event):
        alt_text = '問題六'
        title = '問題六'
        text = '將毛捋順，用手撫摸身體側部，能感受到貓咪腰部曲線嗎?'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to 7
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to 8
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_Q7(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_Q7(self,event):
        global isEnterQ5 = False
        global isEnterQ7 = True
        alt_text = '問題七'
        title = '問題七'
        text = '貓咪腹部有贅肉嗎?'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to F
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to E
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_Q8(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_Q8(self,event):
        global isEnterQ7 = False
        alt_text = '問題八'
        title = '問題八'
        text = '貓咪有行動上面的問題嗎?'
        btn = [
            MessageTemplateAction(
                label = '是',
                text ='是' #go to G
            ),
            MessageTemplateAction(
                label = '否',
                text = '否' #go to F
            ),
        ]
        send_button_message(event.reply_token,alt_text, title, text, btn)

    def is_going_to_resultA(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_resultA(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：A.非常瘦\n您的貓僅有極少量脂肪\n建議：及時尋求獸醫幫助"))

    def is_going_to_resultB(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_resultB(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：B.瘦\n您的貓僅有少量脂肪\n建議：及時尋求獸醫幫助，以確保貓咪得到充足食物。"))

    def is_going_to_resultC(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_resultC(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：C.偏瘦\n您家貓的脂肪含量比理想狀態低\n建議：適當增加對貓的食物供給。"))
    
    def is_going_to_resultD(self,event):
        text = event.message.text
        if text = '否':
            return True
        return False

    def on_enter_resultD(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：D.標準\n您家貓的脂肪含量處於理想狀態中，繼續保持!\n"))

    def is_going_to_resultE(self,event):
        text = event.message.text
        if isEnterQ5 == True:#代表是Q5的result
            if text = '是':
                return True
            return False
        elif isEnterQ5 == False :#代表是Q7的result
            if text = '否':
                return True
            return False

    def on_enter_resultE(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：E.輕度肥胖\n您家貓的脂肪含量比理想狀態稍微偏高。\n建議：請獸醫提供建議，以確保您家的貓攝入適量的食物，避免過量餵食。此外盡量提高貓咪的運動量。"))

    def is_going_to_resultF(self,event):
        text = event.message.text
        if isEnterQ7 == True:#代表是Q7的result
            if text = '是':
                return True
            return False
        elif isEnterQ7 == False :#代表是Q8的result
            if text = '否':
                return True
            return False

    def on_enter_resultF(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：F.中度肥胖\n您家貓的脂肪含量比理想狀態稍微偏高。\n建議：尋求獸醫的幫助，對您的貓咪實施適度的減肥計劃，同時提高貓咪的運動量。"))

    def is_going_to_resultG(self,event):
        text = event.message.text
        if text = '是':
            return True
        return False

    def on_enter_resultG(self,event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="S.H.A.P.E.™ 得分：F.重度肥胖\n您家貓的脂肪含量含量超標，並且正在影響它的健康。\n建議：及時尋求獸醫的幫助，對您的貓咪實施減肥計劃。同時提高貓咪的運動量和健康水平。"))
