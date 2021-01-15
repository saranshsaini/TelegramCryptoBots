import requests
import json
from datetime import datetime
import time
import telebot

#This bot will let you know if the crypto you are watching has dropped below a certain price

TOKEN='##YOUR TELEGRAM KEY HERE##'
bot = telebot.TeleBot(TOKEN)
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
'symbol':'BTC'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '##YOUR CRYPTO KEY HERE##',
}

session = requests.Session()
session.headers.update(headers)
def get_latest_bitcoin_price():
    response = session.get(url, params=parameters)
    response_data = json.loads(response.text)
    final=(response_data['data']['BTC']['quote']['USD']['price'])
    return (round(final, 2))

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/' ##YOUR IFTT URL HERE##

def post_ifttt_webhook(event, value):
    # The data that will be sent to your IFTTT request
    data = {'value1': value}
    # Tell it what you want to do
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the IFTTT Webhook URL
    requests.post(ifttt_event_url, json=data)

#post_ifttt_webhook('bitcoin_price_emergency',100)
minprice=9200
def test():
    if get_latest_bitcoin_price()<=minprice:
        price = get_latest_bitcoin_price()
        date = datetime.now().strftime('%d.%m.%Y %H:%M')
        bot.send_message(chat_id=chatid, text="The BTC price dropped below the threshold! It is currently {} and the price is at ${}".format(date, price))
        time.sleep(5*60)





test()

bot.polling()
