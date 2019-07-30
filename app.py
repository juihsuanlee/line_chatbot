from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


def ask_for_location(event):
    return line_bot_api.reply_message(event.reply_token,
    LocationSendMessage(title='my location', address='Tainan', latitude=22.994821, longitude=120.196452))

def ask_for_buttontemplate(event):
    buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://www.penghu-nsa.gov.tw/FileDownload/Album/Big/20161012162551758864338.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            ),
            URIAction(
                label='uri',
                uri='https://scholar.google.com.tw/'
                )
            ]
        )
    )
    return line_bot_api.reply_message(event.reply_token,buttons_template_message)


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('A83h6LCWCI4nv6Jsz5vNAl+XsKy15SXLfRUxv19R+g3kdBzIsnMJ8Yc4k90MC5r5WfAyo5O+m0NSiTomgu7YtE5V7d4/h8pME2nJirikkjW+QzNxSXzIsBikV1PbPqVjRpCk9DOWuXuRMtwbgdvuCwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('415b0bda341982e4fa53c5b62a406aa1')

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
    temp = event.message.text
    message_encode = temp.encode('utf-8')
    print(message_encode)

    message = TextSendMessage(text=event.message.text)
    
        
    if(event.message.text == "位置"):
        ask_for_location(event)
    elif(event.message.text == "按鈕樣板"):
        ask_for_buttontemplate(event)

        
    reply = requests.get('http://140.115.54.90:10034/give_sentence?sentence='+event.message.text)
    print(reply)
    line_bot_api.reply_message(event.reply_token, reply)



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


