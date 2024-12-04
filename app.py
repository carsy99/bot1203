# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from datetime import datetime
import pytz
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('47Teua1VI1VEw5MKyDF7YEOrJzmMQfsxhpIeWNIl0wza8DUinGMjTfiHO3prD9jdZfj5M8vOJp2tqJkp2sJ4o0A2IDEpBqTeaY57rDl0cRz2FXfQ58yiN6kBgwQSu4qS6hbKxI3TheYLlJFfUDXWJgdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('3474514a3503e0611336ad0b8de26e50')

tz = pytz.timezone('Asia/Taipei')
current_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
line_bot_api.push_message('U6773b925616e46b96db121f79eb2e76d', TextSendMessage(text=f'您好，目前時間是 {current_time} ，請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == "天氣":
        reply = TextSendMessage(text="請稍等，我幫您查詢天氣資訊！")
    
    elif user_message == "心情好":   # 傳送高興心情的貼圖
        reply = StickerSendMessage(package_id='446', sticker_id='1989')  # 開心貼圖
    elif user_message == "心情不好": # 傳送傷心心情的貼圖
        reply = StickerSendMessage(package_id='446', sticker_id='2008')  # 哭泣貼圖

    elif user_message == "找美食":  # 傳送餐廳位置
        reply = LocationSendMessage(
            title="著名餐廳",
            address="433台中市沙鹿區英才路28-1號",
            latitude=24.2265806,
            longitude=120.5741573
        )
    elif user_message == "找景點":  # 傳送景點位置
        reply = LocationSendMessage(
            title="熱門景點",
            address="台北101大樓",
            latitude=25.033976,
            longitude=121.564538
        )

    elif user_message == "熱門音樂":  # 傳送熱門音樂音訊
        reply = AudioSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1J2MmpK7bb4S-HsHx4yC0YeAuoZQhnOag",  
            duration=203000  # 音訊時長 (毫秒)
        )
    elif user_message == "放鬆音樂":  # 傳送放鬆音樂音訊
        reply = AudioSendMessage(
            original_content_url="https://drive.google.com/uc?export=download&id=1LgcJ2bjD8DFakbWY4w6wo8cKyXISuewG",  
            duration=235000  # 音訊時長 (毫秒)
        )
     
    # 新增影片類型處理
    elif user_message == "動作片":
        reply = VideoSendMessage(
            original_content_url="https://campus-studio.com/download/cr.mp4",  # 替換為真實影片連結
            preview_image_url="https://via.placeholder.com/300x200.png?text=MOVE"  # 替換為真實預覽圖連結
        )
    elif user_message == "動畫":
        reply = VideoSendMessage(
            original_content_url="https://example.com/animation_video.mp4",  # 替換為真實影片連結
            preview_image_url="https://via.placeholder.com/300x200.png?text=anime"  # 替換為真實預覽圖連結
        )
    elif user_message == "紀錄片":
        reply = VideoSendMessage(
            original_content_url="https://samplelib.com/lib/preview/mp4/sample-5s.mp4",  # 替換為真實影片連結
            preview_image_url="https://via.placeholder.com/300x200.png?text=Action+Movie"  # 替換為真實預覽圖連結
        )

    elif user_message == "今天是我的生日":
        image_message = ImageSendMessage(
            original_content_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808",
            preview_image_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808"
        )
        text_message = TextSendMessage(text="生日快樂！希望你有個美好的一天 🎉🎂")
        reply = [image_message, text_message]
    
    else:
        reply = TextSendMessage(text="抱歉，沒有這類型的影片。")

    line_bot_api.reply_message(event.reply_token,reply)
    
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
