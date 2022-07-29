from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage,  ImageSendMessage

import pyimgur

from testPic.models import Pic


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
client = pyimgur.Imgur(settings.IMGUR_CLIENT_ID)
# Create your views here.

def index(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("message",event.message)
                print("userid",event.source)
                message = []
                if event.message.type == 'text':
                    userOrder = event.message.text
                    userId= event.source.user_id
                    print(userId)
                    if "註冊" in userOrder:
                        try:
                            unit = Pic.objects.get(userID=userId)
                            text_="帳號已註冊"
                        except:
                            Pic.objects.create(userID=userId)
                            text_="註冊成功，上傳圖片後請輸入'回傳'"
                        message.append(TextSendMessage(text=text_))
                        line_bot_api.reply_message( event.reply_token, message )  
                    elif "回傳" in userOrder:
                        try:
                            unit   = Pic.objects.get(userID=userId)
                            picurl = unit.userPicUrl
                            #print(picurl)
                            #message.append(TextSendMessage(text=picurl))
                            #line_bot_api.reply_message( event.reply_token, message )  
                            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=picurl, preview_image_url=picurl))
                        except:
                            text_= "尚未註冊或尚未上傳圖片"
                            message.append(TextSendMessage(text=text_))
                            line_bot_api.reply_message( event.reply_token, message )  
                        
                        #line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=uploaded_image.link, preview_image_url=uploaded_image.link))
                    else:
                        text_ = "歡迎使用pictureM，註冊後請上傳圖片"
                        message.append(TextSendMessage(text=text_))
                        line_bot_api.reply_message( event.reply_token, message )  
                elif event.message.type == 'image':
                    text_= event.message.id
                    message_content = line_bot_api.get_message_content(text_)
                    userId= event.source.user_id
                    with open('tempFile/temp.jpg', 'wb') as fd:
                        for chunk in message_content.iter_content():
                            fd.write(chunk)
                    try:
                        uploaded_image = client.upload_image('tempFile/temp.jpg', title="test")
                        #print(li)
                        unit = Pic.objects.get(userID=userId)
                        unit.userPicUrl = uploaded_image.link
                        unit.save()
                        text_="圖片上傳完成，請輸入'回傳'"
                    except:
                        text_="圖片上傳失敗，請稍後在試"
                    message.append(TextSendMessage(text=text_))
                    line_bot_api.reply_message(event.reply_token, message) 
                   
             
                                  
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

