from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('xEk2054U5Hmt63G2t4I1lYgo6iTPndl4E35PngVEH2DT5/2v/veu2UWmBwt3k9e3b+57dfVuvGjorUHRphH8j19bStZ8LM8pVebg/i2vDB/t2tva7yqc887zingBUyRaLEKg91FZzCQH8ztjQDMB8gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5315ea843597d595b356436b8432148a')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message = TextSendMessage(text=event.message.text.encode('utf-8'))
    print(message)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
