# -*- coding: utf-8 -*-
from flask import Flask, request, abort, render_template
from driver import init_driver, finish_driver
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
	ApiClient, Configuration, MessagingApi,
	ReplyMessageRequest, PushMessageRequest,
	TextMessage, PostbackAction,
	ImageMessage,
)
from linebot.v3.webhooks import (
	FollowEvent, MessageEvent, PostbackEvent, TextMessageContent
)
import os
import time

## .env ファイル読み込み
from dotenv import load_dotenv
load_dotenv()

## 環境変数を変数に割り当て
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

## Flask アプリのインスタンス化
app = Flask(__name__)

## LINE のアクセストークン読み込み
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

## コールバックのおまじない
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
		app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
		abort(400)

	return 'OK'

## 友達追加時のメッセージ送信
@handler.add(FollowEvent)
def handle_follow(event):
	## APIインスタンス化
	with ApiClient(configuration) as api_client:
		line_bot_api = MessagingApi(api_client)

	## 返信
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text='Thank You!')]
	))
	
## オウム返しメッセージ
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
	## APIインスタンス化
	with ApiClient(configuration) as api_client:
		line_bot_api = MessagingApi(api_client)

	## 受信メッセージの中身を取得
	received_message = event.message.text

	## 返信メッセージ編集（デバッグ用）
	reply = f'driver初期化開始'
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text=reply)]
	))

	driver = init_driver()

	## 返信メッセージ編集（デバッグ用）
	reply = f'driver初期化完了'
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text=reply)]
	))

	url = 'https://datascience-beginer.com/'  # テストでアクセスするURLを指定
	driver.get(url)

	time.sleep(3)
	driver.save_screenshot('./data/test.png')  # アクセスした先でスクリーンショットを取得

	## 返信メッセージ編集
	reply = f'テスト成功'

	## チャット送信
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text=reply)]
	))

	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=ImageMessage(original_content_url="https://its-restrant.onrender.com/data/test.png",
						  preview_image_url="https://its-restrant.onrender.com/data/test.png")
	))

	finish_driver(driver)

	## 返信メッセージ編集（デバッグ用）
	reply = f'driver停止完了'
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text=reply)]
	))
	"""
	## APIを呼んで送信者のプロフィール取得
	profile = line_bot_api.get_profile(event.source.user_id)
	display_name = profile.display_name

	## 返信メッセージ編集
	reply = f'{display_name}さんのメッセージ\n{received_message}'

	## オウム返し
	line_bot_api.reply_message(ReplyMessageRequest(
		replyToken=event.reply_token,
		messages=[TextMessage(text=reply)]
	))
	"""
## 起動確認用ウェブサイトのトップページ
@app.route('/', methods=['GET'])
def toppage():
	return 'Hello world!'

## ボット起動コード
if __name__ == "__main__":
	## ローカルでテストする時のために、`debug=True` にしておく
	app.run(host="0.0.0.0", port=8000, debug=True)
