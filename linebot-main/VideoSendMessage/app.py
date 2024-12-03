# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('6nVcItOmiqSfD/1J+THWsTzvDOfVLHIhtrvlltLU+aNy6Zw9kzK3tZT6oDWs/86Tkronvv4mbchkTNeOKA0djpLLZRF9RiLOWcY7Fulm+hpb3bh/BGiR8bqvvqGxjpQ5HEDWSYfERJzetfN1IbKj8QdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('cb8a9cb5c70b1bed7adf4f521ed713b6')

line_bot_api.push_message('U6a47d7e0a37f2e732e12675f7f8f1762', TextSendMessage(text='你可以開始了'))

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
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        video_message = VideoSendMessage(
            original_content_url='https://campus-studio.com/download/cr.mp4',
            preview_image_url='https://campus-studio.com/download/cr.jpg'
        )
        line_bot_api.reply_message(event.reply_token, video_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
