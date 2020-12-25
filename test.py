import requests
import os
import random
lat = 23.006891
long = 120.214836
GOOGLE_API_KEY = 'AIzaSyDMA-HQJr05I3DJHo4iNQs39rSOUi5EwMA'
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
    restaurant = random.choice(top20_veterinary_care)
restaurant = top20_veterinary_care[random.choice(above4)]
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
print(rating,address,details)
    # 6. 取得餐廳的 Google map 網址
map_url = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(
    lat=restaurant["geometry"]["location"]["lat"],
    long=restaurant["geometry"]["location"]["lng"],
    place_id=restaurant["place_id"]
)
