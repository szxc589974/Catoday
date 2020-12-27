from transitions.extensions import GraphMachine
import os
import json
import requests
import random
import configparser

photoChoice = ['https://i.imgur.com/zFmUfzB.jpg','https://i.imgur.com/elFmbF3.jpg','https://i.imgur.com/DWouK24.jpg','https://i.imgur.com/4eCtfdV.jpg','https://i.imgur.com/CHSYUaw.jpg','https://i.imgur.com/fmu6mi2.jpg','https://i.imgur.com/IJb1d5D.jpg','https://i.imgur.com/NpVX1or.jpg','https://i.imgur.com/CGGsbUo.jpg','https://i.imgur.com/QwngCq5.jpg','https://i.imgur.com/Q7C2H6W.jpg','https://i.imgur.com/17WX1Cb.jpg','https://i.imgur.com/kGHEia2.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/gzcUpay.jpg','https://i.imgur.com/MIUMTjM.jpg','https://i.imgur.com/HadFEcM.jpg','https://i.imgur.com/e5L8ZYI.jpg','https://i.imgur.com/BcjDfdq.jpg','https://i.imgur.com/qARyHTH.jpg','https://i.imgur.com/XDDfrzk.jpg','https://i.imgur.com/lGKspNb.jpg','https://i.imgur.com/GxcjzWn.jpg','https://i.imgur.com/kwA4EzR.jpg','https://i.imgur.com/4Zkd6A4.jpg','https://i.imgur.com/TyE7ssH.jpg','https://i.imgur.com/PYWGuyp.jpg','https://i.imgur.com/ddyGO9T.jpg','https://i.imgur.com/ozllp4R.jpg']
age = [15,24]
for i in range(1,19):
    age.append(age[i]+4)

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    def is_going_to_choice(self):
        return True

    def on_enter_choice(self):
        print("on_choice")
        choice = input("請輸入模式1.轉換 2.照片 3.醫院")
        



    def is_going_to_input_age(self):
        if on_enter_choice.choice == '1':
            return True
        return False

    def on_enter_input_age(self):
        age = input('請輸入貓咪年齡(歲數):')
        print("on_input_age")

    def is_going_to_convert_age(self):
        if on_enter_input_age.age.isnumeric():
            return True
        return False

    def on_enter_convert_age(self):
        covert = on_enter_input_age.age[int(event.message.text)-1]
        replyCovertAge = "轉換成人類歲數為" + str(covert) + "歲"
        print(replyCovertAge)
        print("on_convert_age")

    def is_going_to_send_picture(self):
        if on_enter_choice.choice == '2':
            return True
        return False

    def on_enter_send_picture(self):
        print(random.choice(photoChoice))
        print("on_send_pictures")
