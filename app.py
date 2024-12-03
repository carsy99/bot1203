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
    
    else:
        reply = TextSendMessage(text="很抱歉，我目前無法理解這個內容。")

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
