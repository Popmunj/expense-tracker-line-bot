import os
from linebot.v3 import ( WebhookHandler )
from coll import get_summary, register, log

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient, 
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)


access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
secret = os.getenv('LINE_CHANNEL_SECRET', None)

config = Configuration(access_token=access_token)
handler = WebhookHandler(secret)

def main(event, context):
    try:
        body = event['body']
        sig = event['headers'].get('x-line-signature', '')
        handler.handle(body, sig)
    except Exception as e:
        print(f"Occured exception: {e}")

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    with ApiClient(config) as api_client:
        bot = MessagingApi(api_client)

        try:
            tool, detail = [e for e in event.message.text.split(" ")]
        except ValueError:
            bot.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[
                        TextMessage(
                            text="Invalid command. Please use [Tool] [Detail]"
                        )
                    ]
                )
            )
            return 'OK'
        
        try:

            if tool == "Register" or tool == "register":
                user_id = event.source.user_id
                member = bot.get_profile(user_id=user_id)
                member_name = member.display_name
            
                register(user_id, member_name)
                bot.reply_message(
                    ReplyMessageRequest(
                        replyToken=event.reply_token,
                        messages=[
                            TextMessage(
                                text=f"Registration is complete for {member_name}"
                            )
                        ]
                    )
                )
            
            elif tool == "Summary" or tool == "summary":
                user_id = event.source.user_id
                left_td, left = get_summary(user_id)
                member = bot.get_profile(user_id=user_id)
                member_name = member.display_name
                bot.reply_message(
                    ReplyMessageRequest(
                        replyToken=event.reply_token,
                        messages=[
                            TextMessage(
                                text=f"Summary for {member_name}: \n Left for today: {left_td} \n Left for this month: {left}"
                            )
                        ]
                    )
                )

            elif tool == "Log" or tool == "log":
                user_id = event.source.user_id
                member = bot.get_profile(user_id=user_id)
                member_name = member.display_name
                
                log(user_id, detail)
                bot.reply_message(
                    ReplyMessageRequest(
                        replyToken=event.reply_token,
                        messages=[
                            TextMessage(
                                text=f"Logging is complete for {member_name}"
                            )
                        ]
                    )
                )

        except Exception as e:
            bot.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[
                        TextMessage(
                            text=f"Oops! Something went wrong."
                        )
                    ]
                )
            )
            print(f"Error: {e}")
            


            



